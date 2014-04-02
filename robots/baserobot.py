import sys
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from configparser import ConfigParser
from os.path import dirname, join
from time import sleep


class BaseRobot:

    def __init__(self, log_file='base_robot_log.txt', config_file='base_robot_config.ini',
                 interval=300, log_to_stdout=True, **config_params):
        self.interval = interval
        self.robot_dir = dirname(sys.modules[self.__class__.__module__].__file__)
        self.config_file = join(self.robot_dir, config_file)
        self.log_file = join(self.robot_dir, log_file)
        self.general_config_section = 'general'

        sh = logging.StreamHandler()
        th = TimedRotatingFileHandler(filename=self.log_file, when='d', interval=1, backupCount=7)
        logging_formatter = logging.Formatter(fmt='[{levelname} {asctime}] {message}', datefmt='%H:%M:%S', style='{')
        sh.setFormatter(logging_formatter)
        th.setFormatter(logging_formatter)
        self.logger = logging.getLogger()
        if log_to_stdout:
            self.logger.addHandler(sh)
        self.logger.addHandler(th)
        self.logger.setLevel(logging.INFO)

        with open(self.config_file, 'w') as c_f:
            cp = ConfigParser()
            cp.add_section(self.general_config_section)
            cp.set(self.general_config_section, 'interval', str(self.interval))
            if config_params:
                for k, v in config_params.items():
                    cp.set(self.general_config_section, k, v)
                cp.write(c_f)

                for k, v in config_params.items():
                    setattr(self, k, v)
                has_params = True
            else:
                has_params = False

        self.logger.info('{} STARTED'.format(self.__class__.__name__))
        if not has_params:
            self.logger.warning('Неопределены параметры конфигурации робота')

    def reread_config(self):
        try:
            cp = ConfigParser()
            cp.read(self.config_file)
            for k, v in cp[self.general_config_section].items():
                    setattr(self, k, v)
        except Exception:
            self.logger.error(self._get_tb_info())

    def reset_params(self, params):
        for k, v in params.items():
            setattr(self, k, v)
            self.logger.info('Переустановлен параметр {} = {}'.format(k, v))

    def get_robot_dir(self):
        return self.robot_dir

    def _get_tb_info(self):
        """Задаёт отступы слева для вывода исключений.
         Количество пробелов высчитывается из строки fmt='[%(levelname)-8s %(asctime)s] %(message)s'"""

        tb_info = traceback.format_exc()
        tb_info = tb_info.split('\n')
        space_count = 30
        spaces = '\n' + ' ' * (space_count + 1)  # Пробелы для красивого отступа в logging.error(tb_info)
        tb_info = spaces.join(tb_info)
        return tb_info

    def pause(self):
        self.logger.info('ПАУЗА')
        sleep(float(self.interval))  # атрибут заново устанавливается методом reread_config, поэтому конвертируем.