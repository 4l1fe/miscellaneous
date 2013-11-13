import unittest
from sbis_root import *


class ПользовательTests(unittest.TestCase):

    def setUp(self):
        import dbm
        self.file_sid = dbm.open('C:\TESTS\sid', 'c')
        self.sid = self.file_sid['sid'].decode()
        self.old_password = self.file_sid['old_password'].decode()
        Session.Set(0, self.sid)

    def tearDown(self):
        self.file_sid.close()

    def test_ИдПоЛогину(self):
        id_ = Пользователь.ИдПоЛогину('person1')
        rs = SqlQuery('''SELECT * FROM "Пользователь" WHERE "Логин"='person1' ''')
        self.assertEqual(id_, 758293)
        self.assertEqual(id_, int(rs[0]['@Пользователь']))

    def test_ЗадатьПароль(self):
        id_ = Пользователь.ИдПоЛогину('person1')
        Пользователь.ЗадатьПароль(id_, '123')
        self.assertTrue(САП.Аутентифицировать('person1', '123'))
        # Восстанавливаем старый пароль для последующих тестов.
        Пользователь.ЗадатьПароль(id_, self.old_password)
        
    def test_ПользовательЗаписать(self):
        id_ = Пользователь.ИдПоЛогину('person1')
        rec = Пользователь.Прочитать(id_, None)
        rec.email = 'person1@mail.ru'
        Пользователь.Записать(MoveToSharedPtr(rec))
        relation = Пользователь.СвязиПользователя(id_)
        person = ЧастноеЛицо.Прочитать(int(relation['@Лицо']))
        self.assertEqual(rec.email, person.email)
        
    def test_ОчиститьКэш(self):
        Тест.ПроверкаОчисткиКэша()
        self.assertEqual(КэшированиеМетодов.ОчиститьКэш('Тест.ПроверкаОчисткиКэша', 0), 0)
