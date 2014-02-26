import rpc
from time import sleep
from os.path import dirname, join
from pprint import pprint
from base_robot import BaseRobot


class NotificationExchenger(BaseRobot):

    def call_nearest_reminders(self):
        try:
            cl = rpc.Client(self.inside_address, is_https=True)
            cl.auth(self.user, self.password)
            result = cl.call('Напоминания.СписокБлижайшихСобытий', ДопПоля=None, Навигация=None, Сортировка=None, Фильтр=None)
            return result
        except Exception:
            tb_info = self.get_tb_info()
            print(tb_info)
            self.logger.error(tb_info)
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
            # result = cl.call('ОповещенияПользователей.ДобавитьУведомление', _site='/notice', ИнфСообщение=ИнфСообщение)
            return result
        except Exception:
            tb_info = self.get_tb_info()
            print(tb_info)
            self.logger.error(tb_info)
            return None

    def call_delivery_result(self, delev_res, reminders_dict):
        if delev_res:
            try:
                cl = rpc.Client(self.inside_address, is_https=True)
                cl.auth(self.user, self.password)
                if len(reminders_dict["d"]) == 1:
                    identifiers = reminders_dict["d"][0]
                elif len(reminders_dict) > 1:
                    identifiers = [l[0] for l in reminders_dict["d"]]
                result = cl.call('Напоминания.РезультатРассылки', Список=identifiers)
                return result
            except Exception:
                tb_info = self.get_tb_info()
                print(tb_info)
                self.logger.error(tb_info)
                return None

        return None


def main():
    exchanger_dir = dirname(__file__)
    exchanger_log_dir = join(exchanger_dir, 'ne_log.txt')
    exchanger_conf_dir = join(exchanger_dir, 'ne_config.ini')
    dflt_conf_params = (('inside_address', 'dev-inside.tensor.ru'),  # пары имя\значение по умолчанию
                   ('user', 'Демо'),
                   ('password', 'Демо123'),
                   ('interval', '60'),
                   ('notification_service', 'dev-sms-app'))

    exchanger = NotificationExchenger(log_file=exchanger_log_dir,
                                      config_file=exchanger_conf_dir,
                                      configuration_parameters=dflt_conf_params)
    print('ROBOT STARTED')
    exchanger.logger.info('ROBOT STARTED')
    while True:
        exchanger.reread_config()
        reminders = exchanger.call_nearest_reminders()
        pprint(reminders)
        res = exchanger.call_add_notification(reminders)
        print(res)
        deliv_res = exchanger.call_delivery_result(res, reminders)
        print(deliv_res)
        sleep(int(exchanger.interval))


if __name__ == '__main__':
    main()














    # def __init__(self, log_file='ne_log.txt', config_file='ne_config.ini'):
        # if not exists(config_file):
        #     with open(config_file, 'w', encoding='utf-8') as c_f:
        #         cp = ConfigParser()
        #         cp['GENERAL'] = {}
        #         cp['GENERAL']['inside_address'] = 'dev-inside.tensor.ru'
        #         cp['GENERAL']['user'] = 'Демо'
        #         cp['GENERAL']['password'] = 'Демо123'
        #         cp['GENERAL']['interval'] = '60'
        #         cp['GENERAL']['notification_service'] = 'dev-sms-app'
        #         cp.write(c_f)
        #
        # self.config_file = config_file
        # cp = ConfigParser()
        # cp.read(config_file)
        # self.inside_address = cp['GENERAL']['inside_address']
        # self.user = cp['GENERAL']['user']
        # self.password = cp['GENERAL']['password']
        # self.interval = int(cp['GENERAL']['interval'])
        # self.notification_service = cp['GENERAL']['notification_service']
        # super().__init__(log_file=log_file)

    # def reread_config(self):
    #     try:
    #         cp = ConfigParser()
    #         cp.read(self.config_file)
    #         self.inside_address = cp['GENERAL']['inside_address']
    #         self.user = cp['GENERAL']['user']
    #         self.password = cp['GENERAL']['password']
    #         self.interval = int(cp['GENERAL']['interval'])
    #         self.notification_service = cp['GENERAL']['notification_service']
    #     except Error:
    #         tb_info = self.get_tb_info()
    #         print(tb_info)
    #         self.logger.error(tb_info)