import rpc
from robots.baserobot import BaseRobot


class RobotNotificationExchanger(BaseRobot):

    def call_nearest_reminders(self):
        try:
            cl = rpc.Client(self.inside_address, is_https=True)
            cl.auth(self.user, self.password)
            remiders_dict = cl.call('Напоминания.СписокБлижайшихСобытий', ДопПоля=None, Навигация=None, Сортировка=None, Фильтр=None)
            return remiders_dict
        except Exception:
            self.logger.error(self._get_tb_info())
            return None

    def call_add_notification(self, reminders_dict):
        """Пример reminders_dict
        {"jsonrpc": "2.0",
         "protocol": 2,
         "method": "ОповещенияПользователей.ДобавитьУведомление",
         "params": {
                   "ИнфСообщение": {
                                 "s": {
                                      "Тип": "Число целое",
                                      "Канал": "Запись",
                                      "Примечание": "Строка",
                                      "ИдОблака": "Строка",
                                      "ИдКлиента": "Число целое",
                                      "ИдПользователя": "Число целое",
                                      "ИдЧастноеЛицо": "Число целое"
                                 },
                                 "d": {
                                        "Тип": 5,
                                        "Канал": {"s":{"SMS": "Логическое", "EMAIL": "Логическое", "JABBER": "Логическое"},
                                                  "d":{"SMS": true, "EMAIL": false, "JABBER": true}},
                                        "Примечание": "Совещание у директора в 18-00",
                                        "ИдОблака": "0009",
                                        "ИдКлиента": 56382,
                                        "ИдПользователя": 56439,
                                        "ИдЧастноеЛицо": 47
                                        }
                                 }
                   },
         "id": 1  }"""

        if reminders_dict and reminders_dict.get("d"):
            # common_part = ["inside-tensor.ru", 5, "Ближайшие события"]
            info_mess = {"s": [{"n": "Тип", "t": "Число целое"},
                                # {"n": "ОтправительНазвание", "t": "Текст"},  # надо ли?
                              # {"n": "ТипДокумента", "t": "Текст"},  # надо ли?
                              {"n": "Канал", "t":"Запись"},
                              {"n": "Примечание", "t": "Текст"},
                              {"n": "ИдОблака", "t":"Строка"},
                              {"n": "ИдКлиента", "t": "Число целое"},
                              {"n": "ИдПользователя", "t": "Число целое"},
                              {"n": "ИдЧастноеЛицо", "t": "Число целое"},
                              ]
                        }
            info_mess["d"] = []
            for l in reminders_dict["d"]:
                l.insert(0, 5)  # 5 - Тип
                info_mess["d"].append(l)
        else:
            return None

        try:
            cl = rpc.Client(self.notification_service)
            result = cl.call('ОповещенияПользователей.ДобавитьУведомление', _site='/notice', ИнфСообщение=info_mess)
            return result
        except Exception:
            self.logger.error(self._get_tb_info())
            return None

    def call_delivery_result(self, result, reminders_dict):
        if result:
            try:
                cl = rpc.Client(self.inside_address, is_https=True)
                cl.auth(self.user, self.password)
                if len(reminders_dict["d"]) == 1:
                    identifiers = [reminders_dict["d"][0]]
                elif len(reminders_dict) > 1:
                    identifiers = [l[0] for l in reminders_dict["d"]]
                deliv_res = cl.call('Напоминания.РезультатРассылки', Список=identifiers)
                return deliv_res
            except Exception:
                self.logger.error(self._get_tb_info())
                return None

        return None


def main():
    rne = RobotNotificationExchanger('ner_log.txt', 'ner_config.ini', 5,
                                     inside_address='dev-inside.tensor.ru',
                                     user='Демо',
                                     password='Демо123',
                                     notification_service='dev-sms-app')
    while True:
        rne.reread_config()

        remiders_dict = rne.call_nearest_reminders()
        rne.logger.info(remiders_dict)
        result = rne.call_add_notification(remiders_dict)
        rne.logger.info(result)
        deliv_res = rne.call_delivery_result(result, remiders_dict)
        rne.logger.info(deliv_res)

        rne.pause()


if __name__ == '__main__':
    main()