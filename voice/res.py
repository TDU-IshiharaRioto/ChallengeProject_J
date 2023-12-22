# -*- coding: utf-8 -*-

import socket
import time

host = 'localhost'
port = 10500

def res(word):
    print(word + '○○さん')

#Juliusに接続する準備
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((host,port))

res = ''
while True:
    while(res.find('\n.')==-1):
        res += sock.recv(1024)

    word = ''
    #改行コードで分割
    for line in res.split('\n'):
        index = line.find('WORD=')
        print('OK')
        line = line[index + 6:line.find("",index + 6)]
        if line !='[s]':
            word = word + line

    if word == 'こんにちは':
        res(word)
    
    elif word == 'おはよう':
        res(word)

    res = ''