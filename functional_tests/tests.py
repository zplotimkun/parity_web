import sys
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase

from time import sleep
from unittest import mock

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.get(self.live_server_url)
    def tearDown(self):
        self.browser.quit()

    def register(self):
        pass
    
    
    def login(self):
        home_login_button = self.browser.find_element_by_id('login')
        self.assertEqual(home_login_button.text, '登入')
        home_login_button.click()
        self.assertIn('auth/', self.browser.current_url)
        login_account = self.browser.find_element_by_name('account')
        login_account.send_keys('test@user')
        login_password = self.browser.find_element_by_name('password')
        login_password.send_keys('123456789')
        login_sumit_button = self.browser.find_element_by_id('check-account')
        login_sumit_button.click()
        self.assertIn('http://localhost', self.browser.current_url)

    def test_login(self):
        #查看首頁-標題跟標頭為'Tim parity web'
        self.assertIn('Tim parity web', self.browser.title)
        #進入登入頁面點擊註冊並註冊(先不須認證)
        home_login_button = self.browser.find_element_by_id('login')
        self.assertEqual(home_login_button.text, '登入')
        home_login_button.click()
        self.assertIn('auth/', self.browser.current_url)

        self.assertIn('登入啦', self.browser.title)
        login_register_button = self.browser.find_element_by_id('register')
        self.assertEqual(login_register_button.text, '註冊')
        login_register_button.click()
        self.assertIn('auth/register/', self.browser.current_url)
        self.assertIn(self.browser.title, '註冊啦')

        register_username = self.browser.find_element_by_name('username')
        register_username.send_keys('test_user')
        register_mail = self.browser.find_element_by_name('mail')
        register_mail.send_keys('test@user')
        register_password = self.browser.find_element_by_name('password')
        register_password.send_keys('123456789')
        register_sumit_button = self.browser.find_element_by_id('send_account')
        self.assertEqual('註冊', register_sumit_button.text)
        register_sumit_button.click()
        self.assertIn('auth/', self.browser.current_url)


        #自動回到登入頁面登入
        login_account = self.browser.find_element_by_name('account')
        login_account.send_keys('test@user')
        login_password = self.browser.find_element_by_name('password')
        login_password.send_keys('123456789')
        login_sumit_button = self.browser.find_element_by_id('check-account')
        login_sumit_button.click()
        self.assertIn('http://localhost', self.browser.current_url)
        #待續.......

    @mock.patch('lists.crawlers.crawlers_array')
    def test_search(self, mock_goods):
        self.login()
        #使用搜尋抓取比價商品資料
        home_search_text = self.browser.find_element_by_name('search_text')
        home_search_text.send_keys('google')
        mock_goods.return_value = [
            {'id': 1,
            'keyword': 'google',
            'link': 'https://24h.pchome.com.tw/prod/QFCD4P-D9008WBCU',
            'name': '電腦王',
            'price': 500,
            'store': 'pchome'
            }, 
            {'id': 2,
            'keyword': 'google',
            'link': 'https://24h.pchome.com.tw/prod/QFCD3O-D9008Y0IC',
            'name': 'flick!',
            'price': 999,
            'store': 'pchome'
            },
            {'id': 3,
            'keyword': 'google',
            'link': 'https://24h.pchome.com.tw/prod/DJAG0N-A9006E2KB',
            'name': 'Google整理術',
            'price': 10000,
            'store': 'pchome'
            }]
        home_search_button = self.browser.find_element_by_name('search_b')
        self.assertEqual('搜尋', home_search_button.text)
        home_search_button.click()
        home_print_search = self.browser.find_element_by_name('good_1')
        self.assertEqual('電腦王', home_print_search.text)
        

if __name__ == '__main__':
    unittest.main(warnings='ignore')