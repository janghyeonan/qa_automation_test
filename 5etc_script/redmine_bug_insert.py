# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:58:19 2019

@author: janghyeonan
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from openpyxl import load_workbook
import time

#엑셀 데이터 읽어오기
def excel_data(path):
    load_wb = load_workbook(path, data_only=True)
    load_ws = load_wb['Sheet1']
    all_values = []
    for row in load_ws.rows:
        row_value = []
        for cell in row:
            row_value.append(cell.value)
        all_values.append(row_value)
    return all_values[1:]

#이슈등록
def issue_write (url, url2, iid, pw, excel_file_path):
    _chrome_options = Options() 
    _chrome_options.add_argument('disable-infobars') 
    
    driver_path = 'd:\\python_script\\chromedriver.exe'
    driver = webdriver.Chrome(driver_path,  chrome_options=_chrome_options)
        
    driver.set_page_load_timeout(20)
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(5)
    
    driver.find_element_by_xpath("//*[@id='account']/ul/li[1]/a").click() #로그인 클릭
    
    #로그인 진행
    driver.find_element_by_xpath("//*[@id='username']").send_keys(iid)
    driver.find_element_by_xpath("//*[@id='password']").send_keys(pw)    
    driver.find_element_by_xpath("//*[@id='login-submit']").click()       
    #driver.find_element_by_xpath("//*[@id='login-form']/form/table/tbody/tr[4]/td[2]/input").click() #실제 프로젝트에서 쓰임
    driver.get(url2) #일감등록으로 넘어옴
    
    d = 0 #카운드 값
           
    for i in excel_data(excel_file_path):
        #driver.find_element_by_xpath("//*[@id='issue_tracker_id']/option[2]").click()  #유형 선택            
        driver.find_element_by_xpath("//*[@id='issue_subject']").send_keys(str(i[2])) #제목 입력
        time.sleep(1)            
        driver.find_element_by_xpath("//*[@id='issue_description']").send_keys(str(i[3]) + ' \n\n!'+ str(i[7]) + '!') #설명 입력
        time.sleep(1)            
        #driver.find_element_by_xpath("//*[@id='issue_status_id']/option[2]").click() #상태 입력            
        #driver.find_element_by_xpath("//*[@id='issue_priority_id']/option[3]").click() #우선순위 입력
        #driver.find_element_by_xpath("//*[@id='issue_assigned_to_id']/option[9]").click() #담당자 설정
        driver.find_element_by_xpath("//*[@id='attachments_form']/span/span[2]/input").send_keys('D:\\GIF\\'+str(i[7])) #파일 업로드
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='issue-form']/input[4]").click() #만들고 계속하기
        time.sleep(1)
        d += 1
        print(str(d))

    driver.close()
    driver.quit()

if __name__=='__main__':
    issue_write(
        'http://127.0.0.1/redmine/',
        'http://127.0.0.1/redmine/projects/dev_/issues/new',
        'root',
        'test1234',
        'd:\\python_script\\buglist.xlsx'
        )