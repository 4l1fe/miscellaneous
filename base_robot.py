import rpc
import logging
import traceback
from configparser import ConfigParser, Error
from os.path import exists


class BaseRobot:
    """Класс под общий интерфейс роботов.
       Предоставляет метод перечитывания конфигураци робота, метод отформатированного вывода исключений"""

    def __init__(self, log_file='base_robot_log.txt', config_file='base_robot_config.ini',
                 configuration_parameters=()):
        self.general_section = 'general'
        self.config_file = config_file

        if not exists(self.config_file):
            with open(self.config_file, 'w', encoding='utf-8') as c_f:
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
            for k, v in cp[self.general_section].items():
                    setattr(self, k, v)
        except Error:
            tb_info = self.get_tb_info()
            print(tb_info)
            self.logger.error(tb_info)
        except KeyError:
            tb_info = self.get_tb_info()
            print(tb_info)
            self.logger.error(tb_info)

    def get_tb_info(self):
        """Задаёт отступы слева для вывода исключений.
         Количество пробелов высчитывается из строки fmt='[%(levelname)-8s %(asctime)s] %(message)s'"""

        tb_info = traceback.format_exc()
        tb_info = tb_info.split('\n')
        space_count = 30
        spaces = '\n' + ' ' * (space_count + 1)  # Пробелы для красивого отступа в logging.error(tb_info)
        tb_info = spaces.join(tb_info)
        return tb_info

