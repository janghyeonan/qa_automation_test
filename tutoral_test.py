# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 14:32:14 2019

@author: janghyeonan
"""

#튜토리얼 자동화

from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import os
import sys

_chrome_options = Options() 
_chrome_options.add_argument('disable-infobars') 
#_chrome_options.add_argument('headless')
driver_path = 'd:\\python_script\\chromedriver.exe'

driver = webdriver.Chrome(driver_path,  chrome_options=_chrome_options)
driver.maximize_window()

def click(x, y, z, f):
    global driver
    driver.save_screenshot('d:\\python_script\\Screenshot\\' + f + '\\' +datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.png')
    canvas = driver.find_element_by_xpath("/html/body/canvas")
    ActionChains(driver).move_to_element_with_offset(canvas, x, y).click().perform()
    driver.save_screenshot('d:\\python_script\\Screenshot\\' + f + '\\' +datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.png')
    time.sleep(z)

def tutorial(x):
    global driver
    
    dir_path = 'd:\\python_script\\Screenshot'
    dir_name = str(x)
    os.mkdir(dir_path + "//" + dir_name + "//")   
    
    driver.get('http://192.168.0.159/HM/?user='+x)
 
    print('#로딩 30초')
    time.sleep(30)  
    print('#스핀클릭#대기 6초')
    click(1200, 610, 6, x)
    
    print('#+클릭#대기 2초')
    click(460, 660, 2, x)
    
    print('#스핀클릭#대기 6초')
    click(1200, 610, 6, x)
    
    print('#스핀클릭#대기 15초')
    click(1200, 610, 15, x)
    
    print('#닫기클릭#대기 8초')
    click(1140, 140, 8, x)
    
    print('#레벨업 콜렉트 클릭#대기 20초')
    click(640, 520, 20, x)
    
    print('#휠클릭 (가운데 아무데나)#대기 6초')
    click(640, 350, 6, x)
    
    print('#콜렉트 클릭#대기 4초')
    click(640, 440, 4, x)
    
    print('#닫기버튼 클릭 #대기 4초')
    click(905, 130, 4, x)
    
    print(x + '번 끝났음.!!')
    driver.save_screenshot('d:\\python_script\\Screenshot\\'+ x +'\\'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.png')
    
    driver.close()
    driver.quit()
    
for x in range(31, 33):
   if len(str(x)) == 1:
       x = '00'+ str(x)
   elif len(str(x)) == 2:
       x = '0'+ str(x)
   tutorial(x)
   time.sleep(5)

if __name__=='__main__':
    tutorial(sys.argv[1]) # 실행시 아큐먼트 값변경으로 게임 변경