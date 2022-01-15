import sys
import socket
import os
import time
import json

def animated_loading():

 anime = [".",".","."]

 done = False

 while done is False:
      for i in anime:
       print('Please wait while system is Loading...')
       time.sleep(0.5)
       done = True


ClientSocket = socket.socket()
host = '192.168.253.12'
port = 8888


print("Connecting.....")

try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))


welcome = ClientSocket.recv(2048)
print(welcome.decode("utf-8"))
while True:
    #Client enter Ic Number
    input_ic = input('\nPlease enter your Identity Card: ')
    ClientSocket.send(str.encode(input_ic))
    ResponseIC=ClientSocket.recv(2048)
    print(ResponseIC.decode("utf-8"))

    #Client prompts input data
    purchase = input('Enter your Property Purchase Price: RM ')
    sale = input('Enter your Property Sale Price: RM ')
    owneryear = input ('Enter period of ownership: RM ')

    mydata = {"p": purchase,"s": sale,"o": owneryear}
    sendData = json.dumps(mydata)
    ClientSocket.send(str.encode(sendData))

    value = ClientSocket.recv(2048)
    print(value.decode("utf-8"))

    print("""
                 MENU
                 [1] Yearly property taxes
                 [2] Print out statement
                 [3] Exit
                                         """)


    option = input('Please enter your options: ')
    ClientSocket.send(str.encode(option))
    
ClientSocket.close()
 
