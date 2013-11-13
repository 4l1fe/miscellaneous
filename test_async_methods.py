import sys
import unittest
import os
import json
from time import sleep

sys.path.append('')
from sbis_root import *


class AsyncMethodsTestCase(unittest.TestCase):

    def setUp(self):  # Петля на самого себя, чтобы, вызывая из питона, устанавливалась сессия\конекст.
        self.obj = BLObject('ProxyObj', 'Тест')
        self.callbacks_log = 'D:\callbacks_log.txt'
        self.additional_parameters = Record()
        self.serv_addr = ConfigGet('АдресСервиса')

    def test_01_Локальный_str(self):
        res = self.obj.Invoke("АсинхронныйВызовМетода", 'ProxyObj', 'Локальный_str', '', self.callbacks_log, self.additional_parameters)
        self.assertEqual('метод отработал', res)
        sleep(1)
        with open(self.callbacks_log) as file:
            callback_output = json.load(file)
        self.assertEqual(callback_output['Результат'], 'Результат локального')
        self.assertEqual(callback_output['Метод']['Сервис'], self.serv_addr+'/service/')
        self.assertTrue(callback_output['Метод']['НазваниеМетода'].endswith('Локальный_str'))
        self.assertTrue(callback_output['Параметры']['callbacks_log'], self.callbacks_log)

    def test_02_Локальный_int(self):
        self.additional_parameters.AddInt32('number', 3)
        self.additional_parameters.AddInt32('power', 3)
        res = self.obj.Invoke("АсинхронныйВызовМетода", 'ProxyObj', 'Локальный_int', '', self.callbacks_log, self.additional_parameters)
        self.assertEqual('метод отработал', res)
        sleep(1)
        with open(self.callbacks_log) as file:
            callback_output = json.load(file)
        self.assertEqual(callback_output['Результат'], 3**3)
        self.assertEqual(callback_output['Метод']['Сервис'], self.serv_addr+'/service/')
        self.assertTrue(callback_output['Метод']['НазваниеМетода'].endswith('Локальный_int'))
        self.assertTrue(callback_output['Параметры']['callbacks_log'], self.callbacks_log)
        self.assertTrue(callback_output['Параметры']['number'], 3)
        self.assertTrue(callback_output['Параметры']['power'], 3)

    def test_03_Локальный_float(self):
        res = self.obj.Invoke("АсинхронныйВызовМетода", 'ProxyObj', 'Локальный_float', '', self.callbacks_log, self.additional_parameters)
        self.assertEqual('метод отработал', res)
        sleep(1)
        with open(self.callbacks_log) as file:
            callback_output = json.load(file)
        self.assertEqual(callback_output['Результат'], 12.987)
        self.assertEqual(callback_output['Метод']['Сервис'], self.serv_addr+'/service/')
        self.assertTrue(callback_output['Метод']['НазваниеМетода'].endswith('Локальный_float'))
        self.assertTrue(callback_output['Параметры']['callbacks_log'], self.callbacks_log)

    def test_04_Локальный_bool(self):
        res = self.obj.Invoke("АсинхронныйВызовМетода", 'ProxyObj', 'Локальный_bool', '', self.callbacks_log, self.additional_parameters)
        self.assertEqual('метод отработал', res)
        sleep(1)
        with open(self.callbacks_log) as file:
            callback_output = json.load(file)
        self.assertEqual(callback_output['Результат'], True)
        self.assertEqual(callback_output['Метод']['Сервис'], self.serv_addr+'/service/')
        self.assertTrue(callback_output['Метод']['НазваниеМетода'].endswith('Локальный_bool'))
        self.assertTrue(callback_output['Параметры']['callbacks_log'], self.callbacks_log)

    def test_05_Локальный_error(self):
        res = self.obj.Invoke("АсинхронныйВызовМетода", 'ProxyObj', 'Локальный_error', '', self.callbacks_log, self.additional_parameters)
        self.assertEqual('метод отработал', res)
        sleep(1)
        with open(self.callbacks_log) as file:
            callback_output = json.load(file)
        self.assertEqual(callback_output['Ошибка'], 'simulated local exception')
        self.assertEqual(callback_output['Метод']['Сервис'], self.serv_addr+'/service/')
        self.assertTrue(callback_output['Метод']['НазваниеМетода'].endswith('Локальный_error'))
        self.assertTrue(callback_output['Параметры']['callbacks_log'], self.callbacks_log)

    def test_06_Удаленный_record(self):
        res = self.obj.Invoke("АсинхронныйВызовМетода", 'ProxyObj', 'Удаленный_record', 'ГруппаДляПрокси', self.callbacks_log, self.additional_parameters)
        self.assertEqual('метод отработал', res)
        sleep(1)
        with open(self.callbacks_log) as file:
            callback_output = json.load(file)
        self.assertFalse(callback_output['Результат']['Вторник'])
        self.assertEqual(callback_output['Метод']['Сервис'], self.serv_addr+'/realisation/service/')
        self.assertTrue(callback_output['Метод']['НазваниеМетода'].endswith('Удаленный_record'))
        self.assertTrue(callback_output['Параметры']['callbacks_log'], self.callbacks_log)

    def test_07_Удаленный_recordset(self):
        res = self.obj.Invoke("АсинхронныйВызовМетода", 'ProxyObj', 'Удаленный_recordset', 'ГруппаДляПрокси', self.callbacks_log, self.additional_parameters)
        self.assertEqual('метод отработал', res)
        sleep(1)
        with open(self.callbacks_log) as file:
            callback_output = json.load(file)
        self.assertFalse(callback_output['Результат']['Понедельник'])
        self.assertTrue(callback_output['Результат']['Суббота'])
        self.assertEqual(callback_output['Метод']['Сервис'], self.serv_addr+'/realisation/service/')
        self.assertTrue(callback_output['Метод']['НазваниеМетода'].endswith('Удаленный_recordset'))
        self.assertTrue(callback_output['Параметры']['callbacks_log'], self.callbacks_log)

    @unittest.skip('проверить позже')
    def test_08_Удаленный_rpcfile(self):
        res = self.obj.Invoke("АсинхронныйВызовМетода", 'ProxyObj', 'Удаленный_rpcfile', 'ГруппаДляПрокси', self.callbacks_log, self.additional_parameters)
        self.assertEqual('метод отработал', res)
        sleep(1)
        with open(self.callbacks_log) as file:
            callback_output = json.load(file)
        self.assertEqual(callback_output['Результат'], b'123456789')
        self.assertEqual(callback_output['Метод']['Сервис'], self.serv_addr+'/realisation/service/')
        self.assertTrue(callback_output['Метод']['НазваниеМетода'].endswith('Удаленный_rpcfile'))
        self.assertTrue(callback_output['Параметры']['callbacks_log'], self.callbacks_log)

    def test_09_Удаленный_array(self):
        self.additional_parameters.AddArrayBool('bool_array')
        self.additional_parameters.bool_array = [True, False, False]
        res = self.obj.Invoke("АсинхронныйВызовМетода", 'ProxyObj', 'Удаленный_array', 'ГруппаДляПрокси', self.callbacks_log, self.additional_parameters)
        self.assertEqual('метод отработал', res)
        sleep(1)
        with open(self.callbacks_log) as file:
            callback_output = json.load(file)
        self.assertTrue(any(callback_output['Результат']))
        self.assertEqual(len(callback_output['Результат']), 3)
        self.assertEqual(callback_output['Метод']['Сервис'], self.serv_addr+'/realisation/service/')
        self.assertTrue(callback_output['Метод']['НазваниеМетода'].endswith('Удаленный_array'))
        self.assertTrue(callback_output['Параметры']['callbacks_log'], self.callbacks_log)

    def test_10_Удаленный_error(self):
        res = self.obj.Invoke("АсинхронныйВызовМетода", 'ProxyObj', 'Удаленный_error', 'ГруппаДляПрокси', self.callbacks_log, self.additional_parameters)
        self.assertEqual('метод отработал', res)
        sleep(1)
        with open(self.callbacks_log) as file:
            callback_output = json.load(file)
        self.assertEqual(callback_output['Ошибка'], 'simulated remote exception')
        self.assertEqual(callback_output['Метод']['Сервис'], self.serv_addr+'/realisation/service/')
        self.assertTrue(callback_output['Метод']['НазваниеМетода'].endswith('Удаленный_error'))
        self.assertTrue(callback_output['Параметры']['callbacks_log'], self.callbacks_log)

    def tearDown(self):
        os.remove(self.callbacks_log)


if __name__ == '__main__':
    unittest.main(verbosity=2)