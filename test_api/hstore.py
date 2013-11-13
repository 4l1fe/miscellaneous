import unittest
import os

os.environ['SBIS_PYTHON_UNITTEST'] = '1'
from sbis_root import *

@unittest.skipIf(os.environ['SBIS_PLATFORM_VERSION'] < '3.6.0', 'Тест для версии выше 3.6.0 включительно')
class HstoreTestCase(unittest.TestCase):

    def test_CreateHstore(self):
        """Автор: Рыбаков М.А"""
        hs = CreateHstore({'a': '123', 'b': '456'})

        self.assertEqual(sorted(hs.split(',')), ['"a"=>"123"','"b"=>"456"'])

    def test_ParseHstore(self):
        """Автор: Рыбаков М.А"""
        self.hs = ParseHstore('"a"=>"123","b"=>"456"')

        self.assertEqual(self.hs, {'a':'123','b':'456'})