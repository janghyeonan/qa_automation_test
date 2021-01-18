# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:03:23 2019

@author: janghyeonan
"""

#패치해주는 서버
# -*- coding: utf-8 -*-

import socket 
from _thread import *
import shutil


# 쓰레드에서 실행되는 코드입니다. 
HOST = '192.168.0.99'
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 

def threaded(client_socket, addr): 

    print('접속되었습니다.  :', addr[0], ':', addr[1]) 

    name = str(addr[0])
    if name == '192.168.0.69':
        name = 'PC1'
    elif name == '192.168.0.70':
        name = 'PC2'
    elif name == '192.168.0.71':
        name = 'PC3'
    elif name == '192.168.0.72':
        name = 'PC4'
    
    # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
    while True: 
        try:
            message = input('\n'+name+'에게 패치명령 보내기↑(진행) : \n')    
                
            if message =='':
                message = '입력 내용 없음!'
                print(message)
            elif message =='패치시작':
                shutil.copy2(r'D:\python_script\client1.py', r'D:\flask\app\static\client1.pyp') ##client1
                shutil.copy2(r'D:\python_script\client2.py', r'D:\flask\app\static\client2.pyp') ##client2
                shutil.copy2(r'D:\python_script\client3.py', r'D:\flask\app\static\client3.pyp') ##client3
                shutil.copy2(r'D:\python_script\patch_client.py', r'D:\flask\app\static\patch_client.pyp') ##client3
                print('파일복사를 진행함')
                print('보낸 메시지 ↑: '+ str(message))
                client_socket.send(message.encode())   
            elif message !='':
                print('보낸 메시지 ↑: '+ str(message))
                client_socket.send(message.encode())   

        except ConnectionResetError as e:
            print('\n!!!!! ' + name +' 클라이언가 접속이 종료되었습니다. !!!!! \nDisconnected by ' + addr[0],':',addr[1])
            break

print('패치용 9999포트 서버 시작 ')

# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.
# 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
while True:     
    print('클라이언트 접속하기를 대기 하는 중 ....')
    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr))

server_socket.close() 