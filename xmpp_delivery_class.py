#coding:utf-8

import shelve
import rpc
import sleekxmpp
import time
import json
import base64
import traceback
import logging
from socket import gethostbyname
from contextlib import closing
from copy import deepcopy


#====================================================================#
XMPP_HOST = 'test-autotest4'
XMPP_PORT = 5222
XMPP_SENDER = 'admin@test-autotest4'
XMPP_SENDER_PASSWORD = 'nimda'
XMPP_GROUP = XMPP_HOST + '/announce/all'  # для рассылки всем зарег-ым пользователям.
URL_LEFT_PART = 'http://wi.sbis.ru/questions/redaktirovanie_voprosa?editParams='
URL_COMMON_PARAMS = {'obj': 'Вопрос', 'history': True, 'method': 'СписокВопросов', 'readOnly': False,
                     '_events': {'onLoadError': [], 'onBeforeUpdate': [], 'onBeforeRead': []}}

TIMEOUT = 10 # Время в секундах, по истечении которго будет посылаться запрос на получение данных.


#====================================================================#
class Notifier(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, group, notification):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.notification = notification
        self.group = group

        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.send_message(mto=self.group, mbody=self.notification)
        self.disconnect(wait=True)


class Synchronizer:

    def __init__(self, db_file, log_file):
        self.db_file = db_file
        logging_handler = logging.FileHandler(filename=log_file, mode='a')
        logging_formatter = logging.Formatter(fmt='[%(levelname)-8s %(asctime)s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
        logging_handler.setFormatter(logging_formatter)
        self.logger = logging.getLogger()
        self.logger.addHandler(logging_handler)
        self.logger.setLevel(logging.INFO)

    def get_response_from_wi(self):
        client = rpc.Client('wi.sbis.ru')
        try:
            response = client.call('Вопрос.СписокВопросов', ДопПоля=[], Навигация=None, Сортировка=None,
                                   Фильтр={'d': [True], 's': [{'t': 'Логическое', 'n': 'ТолькоНеРешенные'}]})
            return response
        except Exception:
            self.logger.error(traceback.print_exc())
            response = {}
            return response

    def send_notification(self):
        notification_text = self.get_notification_text()

        if notification_text:
            notifier = Notifier(XMPP_SENDER, XMPP_SENDER_PASSWORD, XMPP_GROUP, notification=notification_text)
            notifier.register_plugin('xep_0030') # Service Discovery
            notifier.register_plugin('xep_0004') # Data Forms
            notifier.register_plugin('xep_0060')
            notifier.register_plugin('xep_0199') # XMPP Ping
            notifier.connect((gethostbyname(XMPP_HOST), XMPP_PORT), use_tls=False)
            notifier.process(block=True)

    def get_notification_text(self):
        response = self.get_response_from_wi()
        with closing(shelve.open(self.db_file, writeback=True)) as db_file:
            return self.synchronization(response, db_file)

    def initialization(self):
        response = self.get_response_from_wi()
        with closing(shelve.open(self.db_file, writeback=True)) as db_file:
            self.synchronization(response, db_file, init=True)

    def form_new_question_text(self, new_questions):
        template = ''
        if new_questions:
            template = '==================НОВЫЕ ВОПРОСЫ==================\n\n'
            for q in new_questions:
                params = URL_COMMON_PARAMS.copy()
                params['pk'] = q[0][0]  # q['0']['0'] - номер вопроса
                params = json.dumps(params).encode()
                params = base64.standard_b64encode(params)
                full_url = URL_LEFT_PART + params.decode()
                template += 'ЗАГОЛОВОК: {title}\n'
                template += 'ТЕКСТ ВОПРОСА: {description}\n'
                template += 'ДАТА: {dt}\n'
                template = template.format(title=q[1], description=q[2], dt=q[7])
                template += full_url
                template += '\n\n'
        return template

    def form_new_answers_text(self, new_answers):
        template = ''
        if new_answers:
            template = '==================НОВЫЕ ОТВЕТЫ==================\n\n'
            for q in new_answers:
                params = URL_COMMON_PARAMS.copy()
                params['pk'] = q[0][0]
                params = json.dumps(params).encode()
                params = base64.standard_b64encode(params)
                full_url = URL_LEFT_PART + params.decode()
                template += 'ПОЛУЧЕН ОТВЕТ НА ВОПРОС: {number} {title}\n'.format(number=q[0], title=q[1])
                template += full_url
                template += '\n\n'
        return template

    def synchronization(self, response, db_file, init=False):
        if init:  # При инициализации только лишь чистим\перезаписываем без рассылки.
            if len(response.get('d', [])) == 0:  # Чистим DATABASE, если все вопросы закрыты\решены.
                db_file['response'] = []
                db_file['last_question'] = []

            if len(response.get('d', [])) > 0:  # Ответ может быть пустой.
                response['d'].reverse()         # Для сортировки по возрастанию даты\времени.
                db_file['response'] = deepcopy(response['d'])  # ключ d - список данных по всем вопросам.
                db_file['last_question'] = deepcopy(response['d'][-1])  # самый свежий

        else:
            n_text = ''
            new_questions = []
            new_answers = []
            if len(response.get('d', [])) == 0:
                db_file['response'] = []
                db_file['last_question'] = []

            if len(response.get('d', [])) > 0:
                response['d'].reverse()
                if not db_file.get('response'):  # Если база пуста, все вопросы пишем и отправляем как новые.(После зелёного экрана)
                    db_file['response'] = deepcopy(response['d'])
                    db_file['last_question'] = deepcopy(response['d'][-1])
                    new_questions.extend(response['d'])
                    n_text += self.form_new_question_text(new_questions)

                else:  # Тут уже детальное сравнение вопросов\ответов.
                    for question in response['d']:
                        if question[7] > db_file['last_question'][7]:
                            new_questions.append(question)
                            db_file['response'].append(question)
                            db_file['last_question'] = question
                    n_text += self.form_new_question_text(new_questions)

                    # Проверяем, закрылись ли какие-либо вопросы в новом ответе response
                    # и есть ли удалённые.
                    # При новых вопросах, длина DATABASE всегда больше.
                    pop_indexes = []
                    if len(db_file['response']) > len(response['d']):
                        received_questions = [response['d'][q][0] for q in range(len(response['d']))]
                        for i, old_question in enumerate(db_file['response']):
                            if old_question[0] not in received_questions:
                                pop_indexes.append(i)
                    for i, index in enumerate(pop_indexes):
                        db_file['response'].pop(index - i)

                    zip_ = zip(db_file['response'], response['d'])  # zip ведёт себя неявно
                    for i, (old_question, question) in enumerate(zip_):  # enumerate ведёт себя неявно
                        if old_question[4] < question[4]:  # 4 - индекс поля "Количество ответов".
                            new_answers.append(question)
                            db_file['response'][i] = deepcopy(response['d'][i])
                    n_text += self.form_new_answers_text(new_answers)

            return n_text


if __name__ == '__main__':
    syncr = Synchronizer(db_file='xmpp_delivery', log_file='xmpp_delivery_log.txt')
    syncr.initialization()
    syncr.send_notification()
    while True:
        syncr.send_notification()
        time.sleep(TIMEOUT)