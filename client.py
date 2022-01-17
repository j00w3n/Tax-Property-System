import sys
import socket
import os
import time
import json

FORMAT = "utf-8"
SIZE = 1024
ClientSocket = socket.socket()

host = '192.168.56.5'
port = 8888


print("Connecting.....")

try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))
#BANNER
welcome = ClientSocket.recv(1024) #recv 1
print(welcome.decode(FORMAT))
banner=ClientSocket.recv(1024) #recv 3
print(banner.decode(FORMAT))
#BANNER

#Client enter Ic Number
input_ic = input('\nPlease enter your Identity Card: ')
ClientSocket.send(str.encode(input_ic)) #send 2 
ResponseIC=ClientSocket.recv(1024) #recv 3
print(ResponseIC.decode(FORMAT))


#Client prompts input data
purchase = input('Enter your Property Purchase Price: RM ')
sale = input('Enter your Property Sale Price: RM ')
owneryear = input ('Enter period of ownership (Year):  ')
#send list of data JSON to server 
mydata = {"p": purchase,"s": sale,"o": owneryear}
sendData = json.dumps(mydata)
ClientSocket.send(str.encode(sendData)) #send 4

while True:

    print("Data has been sent to the server!")

    print("""
                TAX PROPERTY ONLINE SYSTEM

                 MENU
                 [1] Yearly property taxes
                 [2] Print out statement
                 [3] Exit
                                         """)
    option = input('Please enter your options: ') 
    if option == '3':
        break
    else:
        ClientSocket.send(str.encode(option)) #send 6
        if option == '1':
            msg = ClientSocket.recv(1024)
            print(msg.decode(FORMAT))
        if option == '2':
            fn = ClientSocket.recv(1024).decode(FORMAT)
            print(f"Receiving the filename.")
            file = open(fn, "w+")
            fd = ClientSocket.recv(1024).decode(FORMAT)
            print(f"Receiving the file data.")
            file.write(fd)
            file.close()
            
ClientSocket.close()
