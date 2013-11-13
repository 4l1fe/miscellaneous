import sys
import os
import logging
import traceback
import ctypes
import argparse
import subprocess
from threading import Thread
from urllib import request
from datetime import datetime, timedelta
from os.path import join, exists, dirname, abspath
from configparser import ConfigParser, Error
from time import sleep


#==============================================================3
CreateMutex = ctypes.windll.kernel32.CreateMutexA
CloseHandle = ctypes.windll.kernel32.CloseHandle
GetLastError = ctypes.windll.kernel32.GetLastError
ERROR_ALREADY_EXISTS = 183
SIGTERM = 15

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-ppid', '--parent_process_pid', required=True, dest='parent_process_pid', action='store')


#==============================================================#
class Robot:

    def __init__(self, config_file='robot_config.ini', log_file='robot_log.txt', xml_responses_dir='xml_responses_dir'):
        if not exists(config_file):
            with open(config_file, 'w') as c_f:
                cp = ConfigParser()
                cp['GENERAL'] = {}
                cp['GENERAL']['server_ip'] = '10.76.113.44'
                cp['GENERAL']['user'] = 'admin'
                cp['GENERAL']['password'] = 'admin'
                cp['GENERAL']['interval'] = '60'
                cp.write(c_f)

        self.xml_responses_dir = xml_responses_dir
        self.config_file = config_file
        cp = ConfigParser()
        cp.read(config_file)
        self.clock_house_ip = cp['GENERAL']['server_ip']
        self.user = cp['GENERAL']['user']
        self.password = cp['GENERAL']['password']
        self.interval = int(cp['GENERAL']['interval'])
        self.current_datetime = datetime.now()
        self.template_query = 'http://' + self.clock_house_ip + '/query/ta?begin={}&end={}'  # Запрос на приходы\уходы.

        # Настройка логера: файл лога, формат вывода текста в лог.
        logging_handler = logging.FileHandler(filename=log_file, mode='a', encoding='utf-8')
        logging_formatter = logging.Formatter(fmt='[%(levelname)-8s %(asctime)s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
        logging_handler.setFormatter(logging_formatter)
        self.logger = logging.getLogger()
        self.logger.addHandler(logging_handler)
        self.logger.setLevel(logging.INFO)

    def reread_config(self):
        try:
            cp = ConfigParser()
            cp.read(self.config_file)
            self.clock_house_ip = cp['GENERAL']['server_ip']
            self.user = cp['GENERAL']['user']
            self.password = cp['GENERAL']['password']
            self.interval = int(cp['GENERAL']['interval'])
            self.template_query = 'http://' + self.clock_house_ip + '/query/ta?begin={}&end={}'
        except Error:
            tb_info = self.get_tb_info()
            self.logger.error(tb_info)

    def get_tb_info(self):
        '''метод для получения текста отладочной информации с отступами слева'''
        tb_info = traceback.format_exc()
        tb_info = tb_info.split('\n')
        space_count = 30
        spaces = '\n' + ' ' * (space_count+1)  # Пробелы для красивого отступа в logging.error(tb_info)
        tb_info = spaces.join(tb_info)
        return tb_info

    def write_response_to_xml(self, body):
        if not exists(self.xml_responses_dir):
            os.mkdir(self.xml_responses_dir)

        date_dir = self.current_datetime.strftime('%Y_%m_%d')
        date_dir = join(self.xml_responses_dir, date_dir)
        if not exists(date_dir):
            os.mkdir(date_dir)

        file_name = 'reponse_{}'.format(self.current_datetime.strftime('%d%m%Y_%H%M%S.xml'))
        file_name = join(date_dir, file_name)
        file = open(file_name, 'w')
        file.write(body)
        file.close()

    def make_url_opener(self, query, user, password):
        '''метод нужен для настройки аутентификации'''

        psw_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        psw_mgr.add_password(None, query, user, password)
        auth_handler = request.HTTPBasicAuthHandler(psw_mgr)
        opener = request.build_opener(auth_handler)
        return opener

    def get_last_update_time(self):
        import sbis
        dt = sbis.ЭлектроннаяПроходная.ВремяПоследнегоОбновления(self.clock_house_ip)
        if dt is None:  # Сделаем заглушку даты вчерашним днём.
            dt = self.current_datetime - timedelta(days=1)
            return dt

        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M")  # Формат из метода ВремяПоследнегоОбновления()
        return dt

    def get_latest_info(self):
        '''Передавать значения в параметры begin\end нужно классом datetime'''
        begin = self.get_last_update_time()
        end = self.current_datetime

        # Формат строки даты-времени, передаваемой в запрос, должен быть: YYYYMMDDHHmmSS.
        begin = begin.strftime('%Y%m%d%H%M%S')
        end = end.strftime('%Y%m%d%H%M%S')
        self.query = self.template_query.format(begin, end)
        self.logger.info(self.query)

        try:
            opener = self.make_url_opener(self.query, self.user, self.password)
            response = opener.open(self.query)
            xml = response.read().decode('cp1251')
            self.write_response_to_xml(xml)
            return xml
        except Exception:
            tb_info = self.get_tb_info()
            self.logger.error(tb_info)
            xml = None
            return xml

    def save_latest_info(self, xml):
        if xml:
            import sbis
            result = sbis.ЭлектроннаяПроходная.СохранитьДанные(self.clock_house_ip, xml, self.current_datetime)
            self.logger.info('Метод СохранитьДанные() вернул {}'.format(result))
        else:
            self.logger.info('Метод СохранитьДанные() не отработал')


class SingleInstance:

        def __init__(self):
            self.mutexname = 'robot_mutex_name'
            self.mutex = CreateMutex(None, False, self.mutexname)
            self.lasterror = GetLastError()

        def need_terminate(self):
            return self.lasterror != 0 or self.mutex is None

        def __del__(self):
            if self.mutex:
                try:
                    CloseHandle(self.mutex)
                except:
                    pass #print("kernel32 alraedy unloaded!")


#==============================================================#
def check_parent_process_existence(robot_parent__pid, robot_pid):
    while True:
        try:
            process = subprocess.Popen('wmic process get ProcessId', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pids = process.stdout.readlines()
            if robot_parent__pid not in [pid.decode().strip() for pid in pids[1:]]: # на первом месте байты вида b'ProcessId  \r\r\n'
                os.kill(robot_pid, SIGTERM)
        except Exception:
            pass
        sleep(4)


#==============================================================#
def main():
    single_inst = SingleInstance()
    if single_inst.need_terminate():
        sys.exit(0)

    robot_file_dir = abspath(dirname(__file__))
    main_service_dir = dirname(dirname(robot_file_dir))  # На два уровня вверх, чтобы выйти в корень сервиса
    os.chdir(main_service_dir)
    sys.path.append(main_service_dir)  # Без добавления, в некоторых ситуациях не отрабатывало...

    # file = open(join(robot_file_dir, 'robot_runtime_info.txt'), 'w')
    # file.write('main_service_dir = '+main_service_dir+'\n')
    # for p in sys.path:
    #     file.write(p+'\n')
    # file.close()

    import sbis_root as sbis

    results = arg_parser.parse_args()
    robot_parent_pid = results.parent_process_pid
    robot_pid = os.getpid()

    thread = Thread(target=check_parent_process_existence, args=(robot_parent_pid, robot_pid))
    thread.start()

    log_file = join(robot_file_dir, 'robot_log.txt')
    config_file = join(robot_file_dir, 'robot_config.ini')
    xml_responses_dir = join(robot_file_dir, 'xml_responses_dir')
    robot = Robot(log_file=log_file, config_file=config_file, xml_responses_dir=xml_responses_dir)
    robot.logger.info('ROBOT STARTED')
    while True:
        robot.reread_config()
        xml = robot.get_latest_info()
        robot.save_latest_info(xml)
        sleep(robot.interval)

if __name__ == '__main__':
    main()