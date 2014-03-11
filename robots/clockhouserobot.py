import rpc
from urllib import request
from zipfile import ZipFile, ZIP_DEFLATED  # ZIP_DEFLATED тут быстрее всего, но слабже сжимает
from datetime import datetime, timedelta
from os.path import join, exists, getctime
from os import listdir, mkdir, remove
from baserobot import BaseRobot


class ClockHouseRobot(BaseRobot):

    def update_current_datetime(self):
        self.current_datetime = datetime.now()

    def write_response_to_xml(self, xml):
        if not exists(self.xml_responses_dir):
            mkdir(self.xml_responses_dir)

        try:
            zip_name = join('responses', self.current_datetime.strftime('%Y_%m_%d') + '.zip')
            file_name = self.current_datetime.strftime('%H%M%S.xml')
            with ZipFile(zip_name, 'a', compression=ZIP_DEFLATED, allowZip64=True) as zf:
                zf.writestr(file_name, xml)
        except Exception:
            self.logger.error(self._get_tb_info())

    def make_url_opener(self, query, user, password):
        '''метод нужен для настройки аутентификации сервера TempoReale'''

        psw_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        psw_mgr.add_password(None, query, user, password)
        auth_handler = request.HTTPBasicAuthHandler(psw_mgr)
        opener = request.build_opener(auth_handler)
        return opener

    def call_last_update_time(self):
        try:
            cl = rpc.Client(self.service_address, is_https=True)
            cl.auth('Демо', 'Демо123')
            dt = cl.call('ЭлектроннаяПроходная.ВремяПоследнегоОбновления', Идентификатор=self.clock_house_ip)
        except Exception:
            self.logger.error(self._get_tb_info())
            dt = None

        if dt is None:  # Сделаем заглушку даты вчерашним днём.
            dt = self.current_datetime - timedelta(days=1)
            self.logger.info('метод ВремяПоследнегоОбновления вернул None')
            return dt

        self.logger.info('Значение времени последнего обновления - {}'.format(dt))
        dt = datetime.strptime(dt+'00', "%Y-%m-%d %H:%M:%S%z")  # Формат из метода ВремяПоследнегоОбновления()
        return dt

    def get_latest_info(self):
        '''Передавать значения в параметры begin\end нужно классом datetime'''
        begin = self.call_last_update_time()
        end = self.current_datetime

        # Формат строки даты-времени, передаваемой в запрос, должен быть: YYYYMMDDHHmmSS.
        begin = begin.strftime('%Y%m%d%H%M%S')
        end = end.strftime('%Y%m%d%H%M00')
        query = 'http://{}/query/ta?begin={}&end={}'.format(self.clock_house_ip, begin, end)
        self.logger.info(query)

        try:
            opener = self.make_url_opener(query, self.user, self.password)
            response = opener.open(query)
            xml = response.read().decode('cp1251')
            self.write_response_to_xml(xml)
            return xml
        except Exception:
            self.logger.error(self._get_tb_info())
            return None

    def call_save_data(self, xml):
        if xml:
            try:
                cl = rpc.Client(self.service_address, is_https=True)
                cl.auth('Демо', 'Демо123')
                interval_end = self.current_datetime.timestamp()  # Чтобы сериализация в json не ломалась, преобразуем в вещественное число.
                result = cl.call('ЭлектроннаяПроходная.СохранитьДанные', Идентификатор=self.clock_house_ip, файл=xml, КонецИнтервала=interval_end)
                self.logger.info('Метод СохранитьДанные() вернул {}'.format(result))
            except Exception:
                self.logger.error(self._get_tb_info())
        else:
            self.logger.info('Метод СохранитьДанные() не отработал')

    def del_old_xml_responses_dir(self):
        if exists(self.xml_responses_dir):
            for dir_ in listdir(self.xml_responses_dir):
                if datetime.fromtimestamp(getctime(dir_)).month < datetime.now().month:
                    try:
                        remove(dir_)
                        self.logger.info('Удалена папка с ответами - {}'.format(dir_))
                    except Exception:
                        self.logger.error(self._get_tb_info())


def main():
    clhr = ClockHouseRobot(log_file='chr_log.txt',
                           config_file='chr_config.ini',
                           interval=10,
                           clock_house_ip='10.76.120.91',
                           user='admin',
                           password='admin',
                           service_address='dev-inside.tensor.ru',
                           xml_responses_dir = 'xml_responses_dir')
    while True:
        clhr.reread_config()

        clhr.update_current_datetime()
        xml = clhr.get_latest_info()
        clhr.call_save_data(xml)
        clhr.del_old_xml_responses_dir()

        clhr.pause()

if __name__ == '__main__':
    main()