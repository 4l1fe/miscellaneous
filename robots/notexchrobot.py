import rpc
from copy import deepcopy
from operator import contains
from pprint import pprint as pp
from robots.baserobot import BaseRobot


class NotificationExchangerRobot(BaseRobot):

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
            return None

        try:
            results = []
            for info_mess in info_messages:
                cl = rpc.Client(self.notification_service)
                result = cl.call('ОповещенияПользователей.ДобавитьУведомление', _site='/notice', ИнфСообщение=info_mess)
                results.append(result)
            self.logger.info('Результаты добавления уведомлений: ' + str(results))
            return results
        except Exception:
            self.logger.error(self._get_tb_info())
            return []

    def call_delivery_result(self, results, reminders_dict):
        if all(results):
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
    rne = NotificationExchangerRobot(log_file='ner_log.txt',
                                     config_file='ner_config.ini',
                                     interval=30,
                                     inside_address='dev-inside.tensor.ru',
                                     user='Демо',
                                     password='Демо123',
                                     notification_service='dev-sms-app')
    while True:
        rne.reread_config()

        remiders_dict = rne.call_nearest_reminders()
        results = rne.call_add_notification(remiders_dict)
        rne.call_delivery_result(results, remiders_dict)

        rne.pause()


if __name__ == '__main__':
    main()