import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from configparser import ConfigParser
from os.path import dirname, join
from time import sleep


class BaseRobot:

    def __init__(self, log_file='base_robot_log.txt', config_file='base_robot_config.ini',
                 interval=300, robot_filename=__file__, **config_params):
        self.interval = interval
        robot_dir = dirname(robot_filename)
        self.config_file = join(robot_dir, config_file)
        self.log_file = join(robot_dir, log_file)
        self.general_config_section = 'general'

        sh = logging.StreamHandler()
        th = TimedRotatingFileHandler(filename=self.log_file, when='d', interval=1, backupCount=7)
        logging_formatter = logging.Formatter(fmt='[%(levelname)s %(asctime)s] %(message)-80s', datefmt='%H:%M:%S')
        sh.setFormatter(logging_formatter)
        th.setFormatter(logging_formatter)
        self.logger = logging.getLogger()
        self.logger.addHandler(sh)
        self.logger.addHandler(th)
        self.logger.setLevel(logging.INFO)

        # if config_params:
        #     with open(self.config_file, 'w') as c_f:
        #         cp = ConfigParser()
        #         cp.add_section(self.general_config_section)
        #         for k, v in config_params.items():
        #             cp.set(self.general_config_section, k, v)
        #         cp.write(c_f)
        #
        #     for k, v in config_params.items():
        #         setattr(self, k, v)
        #     has_params = True
        # else:
        #     has_params = False
        #
        # self.logger.info('ROBOT STARTED')
        # if not has_params:
        #     self.logger.warning('Неопределены параметры конфигурации робота')

    def reread_config(self):
        try:
            cp = ConfigParser()
            cp.read(self.config_file)
            for k, v in cp[self.general_config_section].items():
                    setattr(self, k, v)
        except Exception:
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

    def pause(self):
        sleep(self.interval)
