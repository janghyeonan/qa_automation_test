# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 14:32:30 2020

@author: janghyeonan
"""
'''
Android Native Script
'''
import os
import unittest
import datetime
from appium import webdriver
import time
from appium.webdriver.common.touch_action import TouchAction

class AndroidTest(unittest.TestCase):
    
    def setUp(self): # 셋업
        "Setup for the test"
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '7.0'
        desired_caps['APP'] = r'C:\\zz\\platforms\\android\\app\\build\\outputs\\apk\\debug\app-debug.apk'
        desired_caps['automationName'] = 'Appium'
        desired_caps['NewCommandTimeout'] = '300'
        desired_caps['deviceName'] = 'galuxy Note8'
        desired_caps['appPackage'] = 'com.zz'
        desired_caps['appActivity'] = 'com.zz.MainActivity'
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        
    def tearDown(self): # 종료
        "Tear down the test"
        self.driver.quit()
 
    def test_single_player_mode(self):
        driver = self.driver
        print(self.driver.get_window_size())
        TouchAction(driver).tap(x=981, y=1067).perform()
        time.sleep(3)
        TouchAction(driver).tap(x=961, y=867).perform()
        time.sleep(3)
        TouchAction(driver).tap(x=931, y=667).perform()
        time.sleep(3)
        TouchAction(driver).tap(x=699, y=1300).perform()
        TouchAction(driver).tap(x=699, y=1300).send_keys('abcdef').perform()
        time.sleep(30)
        self.driver.keyevent(4)
        self.driver.get_screenshot_as_file("종료알림_토스트 내용.png")
        #뒤로가기(백키)
        self.driver.keyevent(4)        
        #종료
 
#---START OF SCRIPT
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidTest)
    unittest.TextTestRunner(verbosity=2).run(suite)