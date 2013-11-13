import os
import unittest
from sbis_root import *

os.environ['SBIS_PYTHON_UNITTEST'] = '1'
SBIS_PLATFORM_VERSION = os.environ['SBIS_PLATFORM_VERSION']

@unittest.skipIf(SBIS_PLATFORM_VERSION < '3.6.0', 'Тесты предназначены для версии платформы выше 3.6.0 включительно')
class TestSqlQuery(unittest.TestCase):
    def test_clean(self):
        """Автор: Рыбаков М.А"""
        res1 = SqlQuery('select * from "Лицо"')
        res2 = SqlQuery(query='select * from "Лицо"')

        self.assertEqual(res1.get().Size(), 15)
        self.assertEqual(res2.get().Size(), 15)

    def test_args(self):
        """Автор: Рыбаков М.А"""
        ans = SqlQuery('select * from "Лицо" where "@Лицо"=$1', 1)

        self.assertEqual(ans.get().Size(), 1)

        self.assertEqual(str(ans.get()[0]['Название']), 'первый')

    def test_rec(self):
        """Автор: Рыбаков М.А"""
        rec = Record()
        rec.AddInt32('1', 3)

        res1 = SqlQuery('select * from "Лицо" where "@Лицо"=$1', rec)
        res2 = SqlQuery('select * from "Лицо" where "@Лицо"=$1 and "Название"=$2', rec, "трусы")
        res3 = SqlQuery('select * from "Лицо" where "@Лицо"=$1', params=rec)
        res4 = SqlQuery(query='select * from "Лицо" where "@Лицо"=$1', params=rec)

        self.assertEqual(res1.get().Size(), 1)
        self.assertEqual(res2.get().Size(), 1)
        self.assertEqual(res3.get().Size(), 1)
        self.assertEqual(res4.get().Size(), 1)

        self.assertEqual(str( res1.get()[0]['Название'] ), "трусы")
        self.assertEqual(str( res2.get()[0]['Название'] ), "трусы")
        self.assertEqual(str( res3.get()[0]['Название'] ), "трусы")
        self.assertEqual(str( res4.get()[0]['Название'] ), "трусы")

    def test_format(self):
        """Автор: Рыбаков М.А"""
        fmt = CreateRecordFormat();
        fmt.AddInt32('@Лицо')

        res1 = SqlQuery('select * from "Лицо"', fmt)
        res2 = SqlQuery('select * from "Лицо" where "@Лицо"=$1', fmt, 1)
        res3 = SqlQuery('select * from "Лицо"', format = fmt)

        ans = Record( { "@Лицо": 1 } )

        self.assertEqual(res1.get().Size(), 15)
        self.assertEqual(res2.get().Size(), 1)
        self.assertEqual(res3.get().Size(), 15)

        self.assertEqual(str(res1.get()[0]), str(ans))
        self.assertEqual(str(res2.get()[0]), str(ans))
        self.assertEqual(str(res3.get()[0]), str(ans))

    def test_rec_format(self):
        """Автор: Рыбаков М.А"""
        r = Record({ 'Название': 'боты' })
        fmt = CreateRecordFormat()
        fmt.AddInt32('@Лицо')

        ans1 = SqlQuery('select * from "Лицо" where "Название"=$1', r, fmt)
        ans2 = SqlQuery('select * from "Лицо" where "Название"=$1', fmt, r)

        res = Record( { '@Лицо': 4 } )

        self.assertEqual(ans1.get().Size(), 1)
        self.assertEqual(ans2.get().Size(), 1)

        self.assertEqual(str(ans1.get()[0]), str(res))
        self.assertEqual(str(ans2.get()[0]), str(res))

    def test_rec_format_args(self):
        """Автор: Рыбаков М.А"""
        r = Record({ '1': 'шапка' })
        fmt = CreateRecordFormat()
        fmt.AddInt32('@Лицо')

        ans1 = SqlQuery('select * from "Лицо" where "Название"=$1 and "@Лицо"=$2', r, fmt, 5)
        ans2 = SqlQuery('select * from "Лицо" where "Название"=$1 and "@Лицо"=$2', fmt, r, 5)

        res = Record( { '@Лицо': 5 } )

        self.assertEqual(ans1.get().Size(), 1)
        self.assertEqual(ans2.get().Size(), 1)

        self.assertEqual(str(ans1.get()[0]), str(res))
        self.assertEqual(str(ans2.get()[0]), str(res))