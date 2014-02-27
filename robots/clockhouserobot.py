import os
import gzip
import traceback
from urllib import request
from datetime import datetime, timedelta
from os.path import join, exists, dirname, abspath, getctime
from os import listdir
from configparser import ConfigParser, Error
from shutil import rmtree
from time import sleep

import rpc
from robots.baserobot import BaseRobot


class ClockHouseRobot(BaseRobot):


    def update_current_datetime(self):
        self.current_datetime = datetime.now()

    def write_response_to_xml(self, xml):
        if not exists(self.xml_responses_dir):
            os.mkdir(self.xml_responses_dir)

        date_dir = self.current_datetime.strftime('%Y_%m_%d')
        date_dir = join(self.xml_responses_dir, date_dir)
        if not exists(date_dir):
            os.mkdir(date_dir)

        file_name = 'reponse_{}'.format(self.current_datetime.strftime('%d%m%Y_%H%M%S.xml.gz'))
        file_name = join(date_dir, file_name)
        gz_file = gzip.open(file_name, 'wb')
        gz_file.write(xml.encode('cp1251'))  #эта кодировка прописана в протоколе TempoReale
        gz_file.close()

    def make_url_opener(self, query, user, password):
        '''метод нужен для настройки аутентификации'''

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
        self.query = 'http://{}/query/ta?begin={}&end={}'.format(self.clock_house_ip, begin, end)
        self.logger.info(self.query)

        try:
            opener = self.make_url_opener(self.query, self.user, self.password)
            response = opener.open(self.query)
            xml = response.read().decode('cp1251')
            self.write_response_to_xml(xml)
            return xml
        except Exception:
            tb_info = self._get_tb_info()
            self.logger.error(tb_info)
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
                tb_info = self._get_tb_info()
                self.logger.error(tb_info)
        else:
            self.logger.info('Метод СохранитьДанные() не отработал')

    def del_old_xml_responses_dir(self):
        for dir_ in listdir(self.xml_responses_dir):
            if datetime.fromtimestamp(getctime(dir_)).month < datetime.now().month:
                try:
                    rmtree(dir_)
                    self.logger.info('Удалена папка с ответами - {}'.format(dir_))
                except Exception:
                    tb_info = self._get_tb_info()
                    self.logger.error(tb_info)


def main():
    chr_ = ClockHouseRobot(log_file='chr_log.txt',
                           config_file='chr_config.ini',
                           interval=600,
                           robot_filename=__file__,
                           clock_house_ip='10.76.120.91',
                           user='admin',
                           password='admin',
                           service_address='dev-inside.tensor.ru')
    while True:
        chr_.reread_config()

        chr_.update_current_datetime()
        xml = chr_.get_latest_info()
        chr_.call_save_data(xml)

        chr_.pause()

if __name__ == '__main__':
    main()