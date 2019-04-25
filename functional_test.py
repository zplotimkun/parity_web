from selenium import webdriver
from time import sleep
import unittest
import sys

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()


    def test_can_start_a_list_and_retrieve_it_later(self):

        #查看首頁-標題跟標頭為'陳廷比價網'
        self.browser.get('http://localhost:8000')
        self.assertIn('陳廷比價網', self.browser.title)
        #進入登入頁面點擊註冊並註冊(先不須認證)

        #自動回到登入頁面登入

        #使用搜尋抓取比價商品資料

        #待續.......
        print('測試成功')


if __name__ == '__main__':
    unittest.main(warnings='ignore')