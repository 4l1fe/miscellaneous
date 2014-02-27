import rpc
import logging
import traceback
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from configparser import ConfigParser, Error
from datetime import datetime
from os.path import exists


class BaseRobot:
    """Класс под общий интерфейс роботов"""

    def __init__(self, log_file='base_robot_log.txt', config_file='base_robot_config.ini',
                 configuration_parameters=()):
        self.general_section = 'general'
        self.config_file = config_file
        self.log_file = log_file

        with open(self.config_file, 'w') as c_f:
            cp = ConfigParser()
            cp.add_section(self.general_section)
            for k, v in configuration_parameters:
                cp.set(self.general_section, k, v)
            cp.write(c_f)

        cp = ConfigParser()
        cp.read(self.config_file)
        for k, v in cp[self.general_section].items():
            setattr(self, k, v)

        #Настройка логера: файл лога, формат вывода текста в лог.
        sh = logging.StreamHandler()
        th = TimedRotatingFileHandler(filename=self.log_file, when='d', interval=1, backupCount=7)
        logging_formatter = logging.Formatter(fmt='[%(levelname)s %(asctime)s] %(message)-80s', datefmt='%H:%M:%S')
        sh.setFormatter(logging_formatter)
        th.setFormatter(logging_formatter)
        self.logger = logging.getLogger()
        self.logger.addHandler(sh)
        self.logger.addHandler(th)
        self.logger.setLevel(logging.INFO)

    def reread_config(self):
        try:
            cp = ConfigParser()
            cp.read(self.config_file)
            for k, v in cp[self.general_section].items():
                    setattr(self, k, v)
        except Error:
            tb_info = self._get_tb_info()
            self.logger.error(tb_info)
        except KeyError:
            tb_info = self._get_tb_info()
            self.logger.error(tb_info)

    def _get_tb_info(self):
        """Задаёт отступы слева для вывода исключений.
         Количество пробелов высчитывается из строки fmt='[%(levelname)-8s %(asctime)s] %(message)s'"""

        tb_info = traceback.format_exc()
        tb_info = tb_info.split('\n')
        space_count = 30
        spaces = '\n' + ' ' * (space_count + 1)  # Пробелы для красивого отступа в logging.error(tb_info)
        tb_info = spaces.join(tb_info)
        return tb_info

