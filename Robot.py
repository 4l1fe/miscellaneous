#encoding: utf-8
import sys
import os
import rpc
import gzip
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


#==============================================================#
class Robot:

    def __init__(self, config_file='robot_config.ini', log_file='robot_log.txt', xml_responses_dir='xml_responses_dir'):
        if not exists(config_file):
            with open(config_file, 'w') as c_f:
                cp = ConfigParser()
                cp['GENERAL'] = {}
                cp['GENERAL']['clock_house_ip'] = '10.76.120.91'
                cp['GENERAL']['user'] = 'admin'
                cp['GENERAL']['password'] = 'admin'
                cp['GENERAL']['interval'] = '300'
                cp['GENERAL']['service_address'] = 'dev-inside.tensor.ru'
                cp.write(c_f)

        self.xml_responses_dir = xml_responses_dir
        self.config_file = config_file
        cp = ConfigParser()
        cp.read(config_file)
        self.clock_house_ip = cp['GENERAL']['clock_house_ip']
        self.user = cp['GENERAL']['user']
        self.password = cp['GENERAL']['password']
        self.interval = int(cp['GENERAL']['interval'])
        self.service_address = cp['GENERAL']['service_address']
        self.query_template = 'http://' + self.clock_house_ip + '/query/ta?begin={}&end={}'  # Запрос на приходы\уходы.

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
            self.clock_house_ip = cp['GENERAL']['clock_house_ip']
            self.user = cp['GENERAL']['user']
            self.password = cp['GENERAL']['password']
            self.interval = int(cp['GENERAL']['interval'])
            self.service_address = cp['GENERAL']['service_address']
        except Error:
            tb_info = self.get_tb_info()
            self.logger.error(tb_info)

    def update_current_datetime(self):
        self.current_datetime = datetime.now()

    def get_tb_info(self):
        '''метод для получения текста отладочной информации с отступами слева'''
        tb_info = traceback.format_exc()
        tb_info = tb_info.split('\n')
        space_count = 30
        spaces = '\n' + ' ' * (space_count + 1)  # Пробелы для красивого отступа в logging.error(tb_info)
        tb_info = spaces.join(tb_info)
        return tb_info

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

    def get_last_update_time(self):
        try:
            cl = rpc.Client(self.service_address, is_https=True)
            cl.auth('Демо', 'Демо123')
            dt = cl.call('ЭлектроннаяПроходная.ВремяПоследнегоОбновления', Идентификатор=self.clock_house_ip)
        except Exception:
            tb_info = self.get_tb_info()
            self.logger.error(tb_info)
            dt = None

        if dt is None:  # Сделаем заглушку даты вчерашним днём.
            dt = self.current_datetime - timedelta(days=1)
            self.logger.info('метод ВремяПоследнегоОбновления вернул None')
            return dt

        print('Значение времени последнего обновления - {}'.format(dt))
        self.logger.info('Значение времени последнего обновления - {}'.format(dt))
        dt = datetime.strptime(dt+'00', "%Y-%m-%d %H:%M:%S%z")  # Формат из метода ВремяПоследнегоОбновления()
        return dt

    def get_latest_info(self):
        '''Передавать значения в параметры begin\end нужно классом datetime'''
        begin = self.get_last_update_time()
        end = self.current_datetime

        # Формат строки даты-времени, передаваемой в запрос, должен быть: YYYYMMDDHHmmSS.
        begin = begin.strftime('%Y%m%d%H%M%S')
        end = end.strftime('%Y%m%d%H%M00')
        self.query = self.query_template.format(begin, end)
        print(self.query)
        self.logger.info(self.query)

        try:
            opener = self.make_url_opener(self.query, self.user, self.password)
            response = opener.open(self.query)
            xml = response.read().decode('cp1251')
            self.write_response_to_xml(xml)
            return xml
        except Exception:
            tb_info = self.get_tb_info()
            print(tb_info)
            self.logger.error(tb_info)
            xml = None
            return xml

    def save_latest_info(self, xml):
        if xml:
            try:
                cl = rpc.Client(self.service_address, is_https=True)
                cl.auth('Демо', 'Демо123')
                interval_end = self.current_datetime.timestamp()  # Чтобы сериализация в json не ломалась, преобразуем в вещественное число.
                result = cl.call('ЭлектроннаяПроходная.СохранитьДанные', Идентификатор=self.clock_house_ip, файл=xml, КонецИнтервала=interval_end)
                print('Метод СохранитьДанные() вернул {}'.format(result))
                self.logger.info('Метод СохранитьДанные() вернул {}'.format(result))
            except Exception:
                tb_info = self.get_tb_info()
                print(tb_info)
                self.logger.error(tb_info)
        else:
            print('Метод СохранитьДанные() не отработал')
            self.logger.info('Метод СохранитьДанные() не отработал')


#==============================================================#
def main():
    robot_file_dir = dirname(abspath(__file__))
    log_file = join(robot_file_dir, 'robot_log.txt')
    config_file = join(robot_file_dir, 'robot_config.ini')
    xml_responses_dir = join(robot_file_dir, 'robot_xml_responses_dir')

    robot = Robot(log_file=log_file, config_file=config_file, xml_responses_dir=xml_responses_dir)
    print('ROBOT STARTED')
    robot.logger.info('ROBOT STARTED')
    while True:
        robot.reread_config()
        robot.update_current_datetime()
        xml = robot.get_latest_info()
        robot.save_latest_info(xml)
        sleep(robot.interval)

if __name__ == '__main__':
    main()