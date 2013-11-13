from http.client import HTTPConnection, HTTPSConnection, OK
from http.cookies import SimpleCookie
from datetime import datetime
import json

class Client:
    "Удалённый вызов методов БЛ"

    def __init__(self, hostname, is_https=False):
        "Инициализация"
        self.hostname = hostname
        self.header = { 'Content-type': 'application/json; charset=UTF-8' }
        self.timepass = {}
        self.connection = HTTPSConnection if is_https else HTTPConnection

    def auth(self, login, password):
        "Авторизация"
        result = self.call('САП.Аутентифицировать', '/auth', login=login, password=password)
        cookie = SimpleCookie()
        cookie['sid'] = result
        self.header['Cookie'] = str(cookie)
        self.header['X-SBISSessionID'] = result
    
    def call(self, method, _site='', **params):
        "Удалённый вызов метода БЛ"
        body = json.dumps({ 'jsonrpc': '2.0', 'protocol': 3, 'method': method, 'params': params })
        # запрашиваем
        connection = self.connection(self.hostname)
        started = datetime.now() # замер времени
        connection.request('POST', _site + '/service/sbis-rpc-service300.dll', body, self.header)
        response = connection.getresponse()
        passed = (datetime.now() - started).total_seconds()
        data = response.read()
        # проверяем
        if response.status is not OK:
            raise Exception('%d %s: %s' % (response.status, response.reason, data.decode()))
        # читаем
        connection.close()
        # разбираем
        answer = json.loads(data.decode())
        if 'error' in answer:
            raise Exception(answer['error']['message'])
        if 'result' not in answer:
            raise Exception('Ответ от сервера не содержит поле "result".')
        # сохраняем замер времени
        if method not in self.timepass:
            self.timepass[ method ] = [ passed ]
        else:
            self.timepass[ method ].append(passed)
        # возвращаем результат
        return answer['result']
