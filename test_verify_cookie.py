import argparse, unittest
from datetime import datetime
from selenium import webdriver
from atf.xmlrunner import *


class SetCookieTestCase(unittest.TestCase):

    driver = webdriver.Firefox()

    def test_set_get_cookie(self):
        self.cookie_name = 'tested_cookie_name'
        self.cookie_value = 'tested_cookie_value'
        self.driver.delete_cookie(self.cookie_name)
        self.driver.get(result.site)
        cookies = self.driver.get_cookies()
        self.assertNotIn(self.cookie_name, [d['name'] for d in cookies])
        
        start = datetime.now()
        is_errors = True
        while ( datetime.now() - start ).seconds < 30:
            try:
                elem = self.driver.find_element_by_css_selector('div[sbisname="SetCookie"] .ws-button-text-element')
                if elem:
                    elem.click()
                    cookies = self.driver.get_cookies()  # cookies - список из словарей с метаданными
                    self.assertIn(self.cookie_name, [d['name'] for d in cookies])
                    self.assertIn(self.cookie_value, [d['value'] for d in cookies])
                    self.driver.delete_cookie(self.cookie_name)
                    is_errors = False
                    break
            except:
                time.sleep(0.3)
        if is_errors:
            self.fail("Не найдена кнопка запуска теста")
            

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-xo', '--xml_output', dest='xml_output')
    parser.add_argument('-s', '--site', dest='site')
    result = parser.parse_args()
    #result = parser.parse_args(['-s', 'http://localhost:3083'])

    suit = unittest.TestLoader().loadTestsFromTestCase(SetCookieTestCase)
    if result.xml_output:
        XMLTestRunner(output=result.xml_output, verbosity=2).run(suit)
    else:
        unittest.TextTestRunner(verbosity=2).run(suit)