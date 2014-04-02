import rpc
import sys
import ctypes
from copy import deepcopy
from baserobot import BaseRobot
from multiprocessing.connection import Listener
from threading import Thread, RLock, Event


CreateMutex = ctypes.windll.kernel32.CreateMutexA
CloseHandle = ctypes.windll.kernel32.CloseHandle
GetLastError = ctypes.windll.kernel32.GetLastError
ERROR_ALREADY_EXISTS = 183
SIGTERM = 15


class SingleInstance:
        """Необходим при событии загрузки модулей БЛ воркерами, чтобы EventsTransferRobot работал в единственном экземпляре.
        Если мьютекс не создавать, то EventsTransferRobot сможет запуститься несколько раз."""
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
                    pass


class EventsTransferRobot(BaseRobot):

    def run_listener(self, params, lock, stop_flag):
        """Приходить могут команды:
        stop
        isalive
        change_parameters"""
        try:
            listener = Listener(('127.0.0.1', 7676))
        except OSError:
            self.logger.error(self._get_tb_info())
            stop_flag.set()
            sys.exit()

        while True:
            with listener.accept() as connection:
                try:
                    msg = connection.recv()
                    lock.acquire()
                    if msg['cmd'] == 'stop':
                        stop_flag.set()
                        connection.send("Работа робота завершается")
                        sys.exit()
                    elif msg['cmd'] == 'isalive':
                        connection.send("Робот уже работает")
                    elif msg['cmd'] == 'change_parameters':
                        for key, val in ((k, v) for k,v in msg['params'].items() if k in params):
                            params[key] = val
                        connection.send(True)

                    connection.send('')
                except Exception:
                    connection.send(str(sys.exc_info()))
                finally:
                    lock.release()

    def call_nearest_reminders(self):
        try:
            cl = rpc.Client(self.inside_address, is_https=True)
            cl.auth(self.user, self.password)
            remiders_dict = cl.call('Напоминания.СписокБлижайшихСобытий', ДопПоля=None, Навигация=None, Сортировка=None,
                                    Фильтр=None)
            return remiders_dict
        except Exception:
            self.logger.error(self._get_tb_info())
            return {}

    def call_add_notification(self, reminders_dict):
        self.logger.info('Ближайшие события: ' + str(reminders_dict))
        results = []
        if reminders_dict:
            info_messages = []
            for values in reminders_dict["d"]:
                info_mess = {"s": [{"n": "Тип", "t": "Число целое"},
                                   {"n": "ИдПользователя", "t": "Число целое"},
                                   {"n": "ИдКлиента", "t": "Число целое"},
                                   {"n": "ИдЧастноеЛицо", "t": "Число целое"},
                                   {"n": "ИдОблака", "t": "Строка"},
                                   {"n": "Примечание", "t": "Текст"},
                                   {"n": "Канал", "t": "Запись"}],
                                   # {"n": "Действие", "Строка"}
                             "d": []}
                new_values = deepcopy(values[4:])
                new_values.insert(0, 5)
                info_mess["d"].extend(new_values)
                info_messages.append(info_mess)
            self.logger.info('Список из отсылаемых параметров ИнфСообщение: ' + str(info_messages))
        else:
            return results

        try:
            for info_mess in info_messages:
                cl = rpc.Client(self.notification_service)
                result = cl.call('ОповещенияПользователей.ДобавитьУведомление', _site='/notice', ИнфСообщение=info_mess)
                results.append(result)
            self.logger.info('Результаты добавления уведомлений: ' + str(results))
            return results
        except Exception:
            self.logger.error(self._get_tb_info())
            return results

    def call_delivery_result(self, results, reminders_dict):
        if results and all(results):
            try:
                cl = rpc.Client(self.inside_address, is_https=True)
                cl.auth(self.user, self.password)
                identifiers = [l[0] for l in reminders_dict["d"]]
                self.logger.info('Идентификаторы успешных уведомлений: ' + str(identifiers))
                deliv_res = cl.call('Напоминания.РезультатРассылки', Список=identifiers)
                self.logger.info('метод РезультатРассылки вернул ' + str(deliv_res))
                return deliv_res
            except Exception:
                self.logger.error(self._get_tb_info())
                return None


def main():
    single_inst = SingleInstance()
    if single_inst.need_terminate():
        sys.exit(0)

    params = {'log_file': 'ner_log.txt',
              'config_file': 'ner_config.ini',
              'interval': 10,
              'log_to_stdout': False,
              'inside_address': 'dev-inside.tensor.ru',
              'user': 'Admin',
              'password': 'AdminSbis123',
              'notification_service': 'dev-sms-app'}
    lock = RLock()
    stop_flag = Event()

    etr = EventsTransferRobot(**params)
    t = Thread(target=etr.run_listener, args=(params, lock, stop_flag))
    t.start()

    while True:
        if stop_flag.is_set():
            sys.exit()

        lock.acquire()
        etr.reset_params(params)
        lock.release()

        remiders_dict = etr.call_nearest_reminders()
        results = etr.call_add_notification(remiders_dict)
        etr.call_delivery_result(results, remiders_dict)

        etr.pause()

if __name__ == '__main__':
    main()