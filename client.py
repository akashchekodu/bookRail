#!usr/bin/python3
from socket import *
import sys

host = 'localhost' # '127.0.0.1' can also be used
port = 2222

sock = socket()
#Connecting to socket
sock.connect((host, port)) #Connect takes tuple of host and port

loop = True
while(loop):
    data = sock.recv(1024)
    print(data.decode())
    if(data.decode() == 'Hi there!, Welcome to Railway Booking System\n' or data.decode().startswith("Error")):
        continue
    choice = input()
    sock.send(str(choice).encode())
    if(choice == 9):
        exit()
        
sys.exit()