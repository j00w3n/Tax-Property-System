#!/usr/bin/env python3

import sys
import socket

ClientSocket = socket.socket()
host = '192.168.56.5'
port = 8888

print("TAX PROPERTY ONLINE SYSTEM")
print("Connecting.....")

try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
cResp = "Client 2 is connected to the server!"
ClientSocket.send(cResp.encode('utf-8'))

print("\n\nWELCOME TO THE TAX PROPERTY ONLINE SYSTEM")

ClientSocket.close()