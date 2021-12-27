#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 13:03:13 2021

@author: alex
"""
import socket
import threading
import sys
import random
import os


bufferSize = 1024


#Client Code
def ReceiveData(sock):
    while True:
        try:
            data,addr = sock.recvfrom(bufferSize)
            print(data.decode('utf-8'))
        except:
            pass

def RunClient(serverIP):
    host = socket.gethostbyname(socket.gethostname())
    port = random.randint(6000,10000)
    print('Client IP->'+str(host)+' Port->'+str(port))
    server = (str(serverIP),5000)
    UDPClientSocket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
    UDPClientSocket.bind((host,port))
    name = 'make connection to the server'
    UDPClientSocket.sendto(name.encode('utf-8'),server)
    threading.Thread(target=ReceiveData,args=(UDPClientSocket,)).start()
    print("What is your request:")
    while True:        
        request = input()
        if request == 'new user':
            print("Enter: user name, user id ")
            user_name, user_id = input().split()
            data = '0' + ' ' + user_name + ' ' + user_id
            UDPClientSocket.sendto(data.encode('utf-8'),server)           
        elif request == 'remove user':
            print("Enter: User name ")
            user_name = input()
            data = '1' + ' ' + user_name
            UDPClientSocket.sendto(data.encode('utf-8'),server)            
        elif request == 'connect to group':
            print("Enter: group name ")
            group_name = input()
            data = '2' + ' ' + group_name
            UDPClientSocket.sendto(data.encode('utf-8'),server)
        elif request == 'disconnect from group':
            print("Enter: Group name ")
            group_name = input()
            data = '3' + ' ' + group_name
            UDPClientSocket.sendto(data.encode('utf-8'),server)
        elif request == 'send message to user':
            print("Enter: user name to whom to sent the messege")
            user_name_toSend = input()  
            print("Enter: The messege")
            mssg = input()
            data = '4' + ' ' + user_name_toSend + ' ' + mssg
            UDPClientSocket.sendto(data.encode('utf-8'),server)
        elif request == 'send message to group':
            print("Enter: group name to sent the messege")
            group_name_toSend = input()  
            print("Enter: The messege")
            mssg = input()
            data = '5' + ' ' + group_name_toSend + ' ' + mssg
            UDPClientSocket.sendto(data.encode('utf-8'),server)        
        #data = input()
        elif request == 'qqq':
            break
    #UDPClientSocket.sendto(data.encode('utf-8'),server)
    UDPClientSocket.close()
    os._exit(1)
#Client Code Ends Here




if __name__ == '__main__':

    RunClient(sys.argv[1])
    