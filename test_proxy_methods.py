import sys
import unittest
import argparse
from atf.xmlrunner import *

sys.path.append('')
from sbis_root import *


pk = 0
class ProxyMethodsTestCase(unittest.TestCase):
    """Цифры в названии теста служит для запуска тестов в заданном порядке"""

    def test_01_Создать(self):
        rec = Record()
        rec.AddString('Name', 'some_name')
        returned_rec = ProxyObj.Создать('', rec)
        self.assertLess(len(rec), len(returned_rec))
        self.assertEqual(rec.Name, returned_rec.Name)

    def test_02_Записать(self):
        global pk
        rec = Record()
        rec.AddString('Name', 'Patroclus')
        rec.AddDate('Дата', datetime.today().date())
        pk = ProxyObj.Записать(rec)
        rs = SqlQuery("""select "Name" from "ProxyDictionary" """)
        self.assertGreater(pk, 0)
        self.assertEqual(rs[0].Name, rec.Name)

    def test_03_Копировать(self):  # Копирует и записывает.
        global pk
        copied_rec = ProxyObj.Копировать(pk)
        self.assertEqual(int(copied_rec['@ProxyDictionary']), pk+1)

    def test_04_Прочитать(self):
        global pk
        rec = ProxyObj.Прочитать(pk, '')
        self.assertEqual(rec.Name, 'Patroclus')

    def test_05_История(self):
        global pk
        rec = Record()
        rec.AddInt64('ИдО', pk)
        rs = ProxyObj.История(None, rec, None, None)
        self.assertGreater(len(rs), 0)

    def test_06_Объединить(self):
        global pk
        rec = Record()
        rec.AddString('Name', 'Afina')
        rec.AddDate('Дата', datetime.today().date())
        new_pk = ProxyObj.Записать(rec)
        res = ProxyObj.Объединить(pk, new_pk)
        new_rec = ProxyObj.Прочитать(new_pk-1, '')
        old_rec = ProxyObj.Прочитать(pk, '')
        self.assertEqual(old_rec.Name, new_rec.Name)

    def test_07_Удалить(self):
        global pk
        ProxyObj.Удалить(pk)
        ProxyObj.Удалить(pk+1)
        rs = SqlQuery("""select * from "ProxyDictionary" """)
        self.assertEqual(0, len(rs))

    def test_08_Произвольный_1(self):
        import string
        res = ProxyObj.Произвольный_1()
        self.assertTrue(any([char in res for char in string.hexdigits]))

    def test_09_Произвольный_2(self):
        random_stop=30
        res = ProxyObj.Произвольный_2(random_stop)
        self.assertIsInstance(res, int)
        self.assertLessEqual(res, random_stop)

    def test_10_Произвольный_3(self):
        res = ProxyObj.Произвольный_3(True)
        self.assertIsInstance(res, bool)
        self.assertTrue(res)

    def test_11_Произвольный_4(self):
        import datetime
        today = datetime.datetime.today()
        res = ProxyObj.Произвольный_4(today)
        self.assertIsInstance(res, datetime.datetime)
        self.assertEqual(today, res)

    def test_12_Произвольный_5(self):
        import random
        fl = random.random()
        res = ProxyObj.Произвольный_5(fl)
        self.assertIsInstance(res, float)
        self.assertAlmostEqual(fl, res, delta=1e-5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-xo', '--xml_output', dest='xml_output')
    result = parser.parse_args()
    suit = unittest.TestLoader().loadTestsFromTestCase(ProxyMethodsTestCase)

    if result.xml_output:
        XMLTestRunner(output=result.xml_output, verbosity=2).run(suit)
    else:
        unittest.TextTestRunner(verbosity=2).run(suit)