# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:11:27 2019

@author: janghyeonan
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities   
from selenium.webdriver.common.action_chains import ActionChains 
import time
import datetime
from PIL import Image, ImageDraw, ImageFont
import os
import pymysql.cursors
from PIL import Image as PILImage
import sys

#파라미터 2개 계정,  stats(0:일반, 1:일반(골드카드), 2:메가, 3:메가(골드카드))

idid = sys.argv[1]
stats = sys.argv[2]
#
#idid = 'qa06'
#stats = '1'

if stats == 0:
    print('일반 빙고')
elif stats == 1:
    print('일반 빙고(골드카드)')

#카운트 함수
def ddm(x, msg):
    print(msg)
    for j in range(1, int(x)):
        print(str(int(x)-j))
        time.sleep(1)  

def db_puid(x):
    global puid
    db = pymysql.connect(host='192.168.0.99', port=3306, user='root', passwd='test', db='game_database', charset='utf8')
    try:
        with db.cursor() as cursor:   
            cursor.execute("SELECT puid FROM player where nickname = '"+x+"';")
            result0 = cursor.fetchall()
            return result0
    finally:
        db.close()    
try:
    puid = db_puid(idid)[0][0]
except:
    print('입력한 닉네임이 없습니다.!')

#폴더 생성하기
folder_name = datetime.datetime.now().strftime("%y%m%d%H%M") +idid+"_dia"+stats
try:
    os.mkdir(r'c:\\qa\\'+folder_name+'\\')
except:    
    os.mkdir(r'c:\\qa\\'+folder_name+'n\\')

##chrome 옵션
_chrome_options = Options() 
_chrome_options.add_argument('disable-infobars') 
driver_path = 'c:\\qa\\chromedriver.exe'
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }
driver = webdriver.Chrome(driver_path, desired_capabilities=d, chrome_options=_chrome_options)
driver.maximize_window()
driver.get('http://192.168.0.99/ZZ/?user=' + idid)
ddm(40,'데일리 해제')
driver.get('http://192.168.0.99/ZZ/?user=' + idid)
ddm(20,'로딩')

def popup(x,y):
    global driver
    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), x, y).click().perform() 

popup(500,600)
popup(990,145)
popup(500,640)
popup(1050,80)
popup(490,620)
popup(1000,100)
popup(490,650)
popup(1040,70)
        
#빙고내용 초기화
def up_db():
    global puid
    con = pymysql.connect(host='192.168.0.99', port=3306, user='root', passwd='password', db='game_database', charset='utf8')
    cur = con.cursor()
    cur.execute("update player set bingo_vars = '' where puid = "+str(puid)+";")
    con.commit()

#DB조회 후 볼 업데이트
def his_data():
    global puid
    db = pymysql.connect(host='192.168.0.99', port=3306, user='root', passwd='password', db='game_database', charset='utf8')
    try:
        with db.cursor() as cursor:   
            cursor.execute("SELECT bingo_vars FROM player where puid = "+str(puid)+";")
            result0 = cursor.fetchall()
            return result0
    finally:
        db.close()    

def up_db2():
    global puid
    a = his_data()[0][0]
    result = a[:a.find('ball_cnt')+10]+str(10)+a[a.find('ball_cnt')+11:]    
    con = pymysql.connect(host='192.168.0.99', port=3306, user='root', passwd='password', db='game_database', charset='utf8')
    cur = con.cursor()
    cur.execute("update player set bingo_vars = '"+result+"' where puid = "+str(puid)+";")
    con.commit()

#메가 빙고를 업데이트 해줘야 한다.   
def up_db2_mega():
    global puid
    a = his_data()[0][0]
    result = a[:a.find('is_mega')+9] + '1}'
    con = pymysql.connect(host='192.168.0.99', port=3306, user='root', passwd='password', db='game_database', charset='utf8')
    cur = con.cursor()
    cur.execute("update player set bingo_vars = '"+result+"' where puid = "+str(puid)+";")
    con.commit()

def wrimg(fn, msg):        
    target_image = Image.open(fn) #이미지 넣기
    fontsFolder =  r'c:\\qa\\'
    selectFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 15)
    draw = ImageDraw.Draw(target_image)    
    draw.text((480,220), msg, fill = 'yellow', font = selectFont)
    target_image.save(fn)    
    img = Image.open(fn)
    area = (478,215,1441,724)
    cropped_img = img.crop(area)
    cropped_img.save(fn)
    print(fn)


#게임 로그 파싱
def conver(x, name):
    global driver
    dd = x 
    try:    
        if '[RECV]' in dd['message'] or '[SEND]' in dd['message']:        
            a = dd['message'][dd['message'].find('['):]        
            log1 = str(a[:24]).replace('{','').replace('\\','').replace(' ','').replace('"','').replace(',','')  
            
            if log1 == "[RECV]:msg:5070":
                if a.find('picked_num') != -1:
                    aa = a.replace('\\','').replace('"','')
                    b = aa[aa.find('picked_num:')+12:]                
                    print(a)
                driver.save_screenshot(r'c:\\qa\\'+folder_name+'\\'+name+'.png')   
                wrimg(r'c:\\qa\\'+folder_name+'\\'+name+'.png',a)
                
            elif log1 == "[RECV]:msg:5068":
                if a.find('picked_num') != -1:
                    aa = a.replace('\\','').replace('"','')
                    b = aa[aa.find('picked_num:')+12:]
                    #print(b[:b.find(']')] + a)                                    
                    print(a)
                driver.save_screenshot(r'c:\\qa\\'+folder_name+'\\'+name+'.png')
                wrimg(r'c:\\qa\\'+folder_name+'\\'+name+'.png',a)
     
    except Exception as ex: # 에러 종류
            print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름을 받아오는 변수
        
def log_see(name):
    global driver
    b = driver.get_log('browser')
    if b != []:
        num = len(b)
        for i in range(0, num):
            conver(b[i], name)

############## =========== main =====================            
if __name__=='__main__': #인터프리트에서 작업하는 곳
    for z in range(1, 101):
        up_db()#빙고값을 널로 잡고        
        driver.get('http://192.168.0.99/ZZ/?user=' + idid)#화면을 켜서 빙고값이 들어가고
        ddm(20, '웹페이지 로딩')
        
        #로비에서 빙고창을 띄우고
        ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 960, 660).click().perform()        
        ddm(15, '빙고판 연출')
        
        if str(stats) =='1':
            ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 645, 505).click().perform()
            ddm(15, '골드카드 연출')
        
        #다이아 사용하기
        for i in range(1, 7):
            ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 955, 500).click().perform()
            ddm(15, '스크린샷 찍을때 대기시간')
            log_see(str(i))#로그저장 및 스크린샷
            
        #이미지 합쳐서 저장 963 509
        result = Image.new("RGB",(963,3054))
        try:
            result.paste( im = PILImage.open(r'c:\\qa\\'+folder_name+'\\1.png'), box=(0, 0))
            result.paste( im = PILImage.open(r'c:\\qa\\'+folder_name+'\\2.png'), box=(0, 509))
            result.paste( im = PILImage.open(r'c:\\qa\\'+folder_name+'\\3.png'), box=(0, 1018))
            result.paste( im = PILImage.open(r'c:\\qa\\'+folder_name+'\\4.png'), box=(0, 1527))
            result.paste( im = PILImage.open(r'c:\\qa\\'+folder_name+'\\5.png'), box=(0, 2036))
            result.paste( im = PILImage.open(r'c:\\qa\\'+folder_name+'\\6.png'), box=(0, 2545))
        except Exception as ex: # 에러 종류
            print(ex) # ex는 발생한 에러의 이름을 받아오는 변수
        
        if str(stats) =='0':
            result.save(r'c:\\qa\\'+folder_name+'\\dia_nor'+str(z)+'.png')
        elif  str(stats) =='1':
            result.save(r'c:\\qa\\'+folder_name+'\\dia_gold_'+str(z)+'.png')
            
        try:
            os.remove(r'c:\\qa\\'+folder_name+'\\1.png')
            os.remove(r'c:\\qa\\'+folder_name+'\\2.png')
            os.remove(r'c:\\qa\\'+folder_name+'\\3.png')
            os.remove(r'c:\\qa\\'+folder_name+'\\4.png')
            os.remove(r'c:\\qa\\'+folder_name+'\\5.png')
            os.remove(r'c:\\qa\\'+folder_name+'\\6.png')
        except Exception as ex: # 에러 종류
            print(ex) # ex는 발생한 에러의 이름을 받아오는 변수
    
    driver.close()
    print('=================== 테스트 완료 =====================')