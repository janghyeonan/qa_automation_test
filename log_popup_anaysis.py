# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:47:28 2020

@author: janghyeonan
"""
#목적 : 클라이언트를 켜면, 데일리스핀 진행 후 로비 진입, 그리고 데일리 스핀이 끝났다면, 로비 진입 시 팝업을 닫는것을 목적으로 한다.

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities    
from selenium.webdriver.common.action_chains import ActionChains 
import re
import time
import sys
from pandas import DataFrame
import pytest
import random

#! 웹 브라우저 켬
ff = 'qa01' #sys.argv[1] #qa03 #
fffff = 0 #sys.argv[2] #0~7 #위치0

slot_cnt = 2  # 슬롯 돌리는 횟수
#첫번째는 계정, 두번째는 슬롯번호, 스핀  세번째는 화면 위치
account = str(ff)
locate = int(fffff)


#클라이언트 화면 배치좌표
po_x = [-6, 954, -6, 954, 1914, 2874, 1914, 2874]
po_y = [-100, -100, 475, 475, -90, -90, 475, 475 ]
popup_xy = {1:[570,395], 2:[643, 24], 3:[380, 345], 20038:[670, 50], 20039:[670, 50], 20040:[670, 50], 20041:[670, 50] , 20020:[580, 80], 20005:[620, 50], 20006:[620, 50], 20007:[620, 50], 20024:[670,48], 20025:[670,48], 104:[590, 60], 105:[593, 60]}

#슬롯명
slist = ["HitCoin","GenieBlessing","BlackPearl","Childhood","Panda","WolfJackpot","Jewel","PearlOfDragon","TreasureOfEgypt","HotChilliDeluxe","DiamondLuck","MagicIsland","AztecWarrior","KingSavana","HitGold","BloodHunter","Leprechaun","AmericanStars","WildHot","OzCash","ZeusJackpot","GoldFortune","GodOfWealth","Halloween","PirateOfLink","Cinderella","XmasSurprise","LegendOrb","RisingGolds","GiantBuffalo","GFLink",'MysteryGoldMine','AngryPenguin']

lst =[0] #팝업 클릭 순서 번호 담아두는 리스트
first_stats = 0 #데일리 스핀인지, 일반 팝업인지 판단    

#셋업 및 실행
driver_path = 'c:\\qa\\chromedriver.exe'
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }

@pytest.fixture()
def setup():
    global driver
    driver = webdriver.Chrome(driver_path, desired_capabilities=d)   
    
    driver.set_window_position(po_x[locate], po_y[locate])
    driver.get('http://192.168.0.99/zz/?user='+ account)
    driver.set_window_size(974, 625)
    driver.execute_script('document.getElementById("pixiCanvas").style.width = "760px"')
    driver.execute_script('document.getElementById("pixiCanvas").style.height = "427px"')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    driver.execute_script('''
    function getTimeStamp() {
    var d = new Date();
    var s =
    leadingZeros(d.getFullYear(), 4) + '-' +
    leadingZeros(d.getMonth() + 1, 2) + '-' +
    leadingZeros(d.getDate(), 2) + ' ' +
    leadingZeros(d.getHours(), 2) + ':' +
    leadingZeros(d.getMinutes(), 2) + ':' +
    leadingZeros(d.getSeconds(), 2);
    return s;
    }
    function leadingZeros(n, digits) {
    var zero = '';
    n = n.toString();
    if (n.length < digits) {
    for (i = 0; i < digits - n.length; i++)
    zero += '0';
    }
    return zero + n;
    }
    function getMousePosition(canvas, event) { 
    let rect = canvas.getBoundingClientRect(); 
    let x = event.clientX - rect.left; 
    let y = event.clientY - rect.top; 
    console.log("[KEY PRESS] x:"+x+",y:" + y + ' Dt:' + getTimeStamp()); 	
    }
    let canvasElem = document.querySelector("canvas");           
    canvasElem.addEventListener("mousedown", function(e) 
    { 
    getMousePosition(canvasElem, e); 
    }); ''')
    yield
    driver.close()

#프로토콜로 데일리스핀 및 로비 진입 후 팝업 판단.
def popup_click(xx):        
    global popup_xy
    global driver
    if xx == '2':
        ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), popup_xy[int(xx)][0], popup_xy[int(xx)][1]).click_and_hold().perform()
        ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), popup_xy[int(xx)][0], popup_xy[int(xx)][1]).click().perform()
    else:
        ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), popup_xy[int(xx)][0], popup_xy[int(xx)][1]).click().perform()
    time_count(2)
 
def time_count(x):
    for i in range(0, x):        
        time.sleep(1)

def gogo(x_name):
    time_count(10) #10초 기다리기
    lst = [0]
    cntt = 0
    zzz = 999
    html = '''<html><head>
    <style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  
  text-align: left;    
}
</style><title>test log</title></head><body><table>'''
    while zzz < 1000:
        b = driver.get_log('browser')
        if b != []:
            num = len(b)
            for i in range(0, num):            
                result = b[i]['message'].replace('{','').replace('}','').replace('\\','').replace('"','')            
                #6005 팝업
                if 'msg:6005' in result[result.find('msg'):].split(',')[0]: 
                    if len(re.compile(r'product_id:\d+').findall(result.replace('"',''))) == 1:                        
                        if re.compile(r'product_id:\d+').findall(result.replace('"',''))[0] == 'product_id:20008': #핫딜일때
                            time_count(5)
                            ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 611, 75).click().perform() #핫딜 클릭                            
                        else:
                            [lst.append(i.replace('product_id:','')) for i in (re.compile(r'product_id:\d+').findall(result.replace('"','')))]                
                    else:
                        [lst.append(i.replace('product_id:','')) for i in (re.compile(r'product_id:\d+').findall(result.replace('"','')))]          
                #팝업 실행 및 슬롯 이동 페이지 여기서 슬롯을 쳐서 간다.
                if 'msg:5047' in result[result.find('msg'):].split(',')[0]:
                    [lst.append(j.replace('id:','')) for j in (re.compile(r'id:\d+').findall(result.replace('"','')))]
                    print(lst)
                    for i in lst:
                        if i != 0:            
                            popup_click(i)
                    time_count(3)
                    lst =[0] 
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 518, 344).click().perform() # 슬롯 이동 페이지 클릭
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 518, 344).send_keys(x_name).perform()
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 580, 348).click().perform() # 슬롯 이동 페이지 클릭
                #데일리 스핀 체크 구간
                if 'msg:2045' in result[result.find('msg'):].split(',')[0]:#데일리 스핀
                    print('데일리스핀')     
                    time_count(25)
                    popup_click('1')
                    time_count(3)
                    popup_click('2')
                    time_count(3)
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 380, 345).click().perform()
                    time_count(4)
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 621, 128).click_and_hold().perform()
                    time_count(3)
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 650, 99).click().perform()                     
                #로딩이 종료된걸 알려주자.
                if result == "http://192.168.0.199/HM/Common/src/Particle/ParticleSystem.js 142:16 FLARE_FLASH2":#끝난걸 기억해 찾고 값을 기억하자                
                    print('로딩 종료.')                    
                if 'msg:2031' in result[result.find('msg'):].split(',')[0]:# 슬롯입장
                    print('슬롯 입장 시도')
                    time_count(15)
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 661, 374 ).click_and_hold().perform()#스핀 661, 374 
                    time_count(1)
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 661, 374 ).click().perform()
                    time_count(5)
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 661, 220).click().perform()#무한 스
                    print('슬롯 입장 완료.')            
                if 'msg:3020' in result[result.find('msg'):].split(',')[0]:# 이모티콘
                    zzz = 1001
                if 'msg:1002' in result[result.find('msg'):].split(',')[0]:
                    time_count(5)
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 380, 355).click().perform()#무한 스
                if 'msg:4002' in result[result.find('msg'):].split(',')[0]:# 이모티콘
                    time.sleep(15)
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 385, 294).click().perform()#보너스 게임 클
                    time.sleep(15)
                    ActionChains(driver).move_to_element_with_offset(driver.find_element_by_xpath("//*[@id='mainView']/canvas"), 385, 294).click().perform()#보너스 게임 클
                if 'msg:3006' in result[result.find('msg'):].split(',')[0]:# 로그 출력
                    if cntt == slot_cnt:
                        zzz= 1001
                    cntt = cntt +1
                    print('현재 ' + str(cntt) + '번째 스핀입니다.')
                    syms = []
                    if 'syms' in result:
                        for i in result[result.find('[[')+2:result.find(']]')].split('],['):
                            syms.append(i.split(','))                    
                    sysms = DataFrame([[a for a in reversed(j)] for j in syms]).T                    
                    for i in range(0, len(sysms[0])):
                        if i == 2:
                            html = html +"<tr style='background:yellow'>"                        
                        else:
                            html = html +"<tr>"
                        for j in range(0, len(sysms.loc[0])):                            
                            html = html +"<td>" + "<img src='"+x_name+"/"+str(sysms[j][i])+".png'></td>"                            
                        html = html +"</tr>"                            
                    if len(sysms.columns) == 5:
                        sysms.columns=[' ',' ',' ',' ',' ']
                    elif len(sysms.columns) == 4:
                        sysms.columns=[' ',' ',' ',' ']
                    elif len(sysms.columns) == 3:
                        sysms.columns=[' ',' ',' ']
                        
                    if len(sysms) == 5:
                        sysms.index =['','','','','']
                    elif len(sysms) == 4:
                        sysms.index =['','','','']
                    elif len(sysms) == 3:
                        sysms.index =['','','']                    
                    print(sysms)
                    print(result)
                    #html = html + "<tr><td colspan='3'>"+sysms+"</td></tr>"
                    result = result[result.find('msg:'):] 
                    html = html + "<tr><td colspan='3'>"+(result[:result.find('syms:')] + result[result.find('poLv'):]).replace(',','<br />')+"</td></tr>"                        
    html = html + "</table></body></html>"
    loglog = open('D:\\python_script\\loglog_'+x_name+'.html', 'w')
    loglog.write(str(html))
    loglog.close()

def test_slot1(setup):
    global ff
    name = slist[31]
    print('슬롯명 : ' + name)
    ff = 'qa095'
    gogo(name)

def test_slot2(setup):
    global ff
    name = slist[1]
    print('슬롯명 : ' + name)
    ff = 'qa094'
    gogo(name)    

def test_slot3(setup):
   name = slist[2]
   print('슬롯명 : ' + name)
   gogo(name)    

def test_slot4(setup):
   name = slist[3]
   print('슬롯명 : ' + name)
   gogo(name)    

def test_slot5(setup):
   name = slist[4]
   print('슬롯명 : ' + name)
   gogo(name)    

def test_slot6(setup):
   name = slist[5]
   print('슬롯명 : ' + name)
   gogo(name)    

def test_slot7(setup):
   name = slist[6]
   print('슬롯명 : ' + name)
   gogo(name)    

def test_slot8(setup):
   name = slist[7]
   print('슬롯명 : ' + name)
   gogo(name)

#def test_slot9(setup):
#    name = slist[8]
#    print(name)
#    gogo(name)
#
#def test_slot10(setup):
#    name = slist[9]
#    print(name)
#    gogo(name)
#
#def test_slot11(setup):
#    name = slist[10]
#    print(name)
#    gogo(name)
#
#def test_slot12(setup):
#    name = slist[11]
#    print(name)
#    gogo(name)
#
#def test_slot13(setup):
#    name = slist[12]
#    print(name)
#    gogo(name)
#
#def test_slot14(setup):
#    name = slist[13]
#    print(name)
#    gogo(name)
#
#def test_slot15(setup):
#    name = slist[14]
#    print(name)
#    gogo(name)
#
#def test_slot16(setup):
#    name = slist[15]
#    print(name)
#    gogo(name)
#
#def test_slot17(setup):
#    name = slist[16]
#    print(name)
#    gogo(name)
#
#def test_slot18(setup):
#    name = slist[17]
#    print(name)
#    gogo(name)
#
#def test_slot19(setup):
#    name = slist[18]
#    print(name)
#    gogo(name)
#
#def test_slot20(setup):
#    name = slist[19]
#    print(name)
#    gogo(name)
#
#def test_slot21(setup):
#    name = slist[20]
#    print(name)
#    gogo(name)
#
#def test_slot22(setup):
#    name = slist[21]
#    print(name)
#    gogo(name)
#
#def test_slot23(setup):
#    name = slist[22]
#    print(name)
#    gogo(name)
#
#def test_slot24(setup):
#    name = slist[23]
#    print(name)
#    gogo(name)
#
#def test_slot25(setup):
#    name = slist[24]
#    print(name)
#    gogo(name)
#
#def test_slot26(setup):
#    name = slist[25]
#    print(name)
#    gogo(name)
#
#def test_slot27(setup):
#    name = slist[26]
#    print(name)
#    gogo(name)
#
#def test_slot28(setup):
#    name = slist[27]
#    print(name)
#    gogo(name)
#
#def test_slot29(setup):
#    name = slist[28]
#    print(name)
#    gogo(name)
#
#def test_slot30(setup):
#    name = slist[29]
#    print(name)
#    gogo(name)
#
#def test_slot31(setup):
#    name = slist[30]
#    print(name)
#    gogo(name)
