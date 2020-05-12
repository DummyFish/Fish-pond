import sys
import logging
import telnetlib
import time
import argparse
from socket import socket, AF_INET, SOCK_STREAM

VERSION = '1'
welcome = b"login: "

def send_email(src_address):
    pass

def telnet(address,port=23):
    try:
        ski=socket(AF_INET,SOCK_STREAM)
        ski.bind((address, port))
        ski.listen()
        conn,addr = ski.accept()
        print('visited' + addr[0])
        send_email(addr[0])
        conn.sendall(welcome)
        while True:
            data=conn.recv(1024)
            if data == b'\r\n':
                ski.close()
                sys.exit()
    except: 
        ski.close()
        sys.exit()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='honeypot telnet',
                                 epilog='Version: ' + str(VERSION))
    parser.add_argument('-a','--address',help='server ip address to use',action='store', required=True)   
    args = parser.parse_args()
    
    telnet(args.address)
