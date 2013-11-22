import argparse
import unittest
from selenium import webdriver
from atf.xmlrunner import *


class SetCookieTestCase(unittest.TestCase):
    """Цифры в названии теста служит для запуска тестов в заданном порядке"""

    driver = webdriver.Firefox()

    def test_01_set_cookie(self):
        self.driver.get(result.site)
        cookies = self.driver.get_cookies()
        self.assertNotIn(result.cookie_name, cookies)
        query = '''blobj = $ws.proto.BLObject("CookieObj");
                   blobj.call('SetCookie', {'cookie_name': '%s', 'cookie_value': '%s'}, $ws.proto.BLObject.RETURN_TYPE_ASIS)'''
        query = query % (result.cookie_name, result.cookie_value)
        self.driver.execute_script(query)

    def test_02_get_cookie(self):
        cookies = self.driver.get_cookies()  # cookies - список из словарей с метаданными
        self.driver.delete_cookie(result.cookie_name)
        self.driver.close()
        self.assertIn(result.cookie_name, [d['name'] for d in cookies])
        self.assertIn(result.cookie_value, [d['value'] for d in cookies])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-xo', '--xml_output', dest='xml_output')
    parser.add_argument('-s', '--site', dest='site')
    parser.add_argument('-cn', '--cookie_name', dest='cookie_name')
    parser.add_argument('-cv', '--cookie_value', dest='cookie_value')
    result = parser.parse_args()
    #result = parser.parse_args(['-s', 'http://localhost:1001', '-cn', 'some_name', '-cv', 'some_value'])

    suit = unittest.TestLoader().loadTestsFromTestCase(SetCookieTestCase)
    if result.xml_output:
        XMLTestRunner(output=result.xml_output, verbosity=2).run(suit)
    else:
        unittest.TextTestRunner(verbosity=2).run(suit)