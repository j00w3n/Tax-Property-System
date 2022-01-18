import sys
import socket
import os
import time
import json
import signal

FORMAT = "utf-8"
SIZE = 1024
ClientSocket = socket.socket()
host = '192.168.253.12'
port = 8888

print("Connecting.....")

try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

#BANNER
welcome = ClientSocket.recv(SIZE) #recv 1
print(welcome.decode(FORMAT))
banner=ClientSocket.recv(SIZE) #recv 3
print(banner.decode(FORMAT))
#BANNER

#Client enter Ic Number
try:
    input_ic = input('Please enter your Identity Card: ')
    ClientSocket.send(str.encode(input_ic)) #send 2 
    ResponseIC=ClientSocket.recv(SIZE) #recv 3
    print(ResponseIC.decode(FORMAT))
except KeyboardInterrupt:
    print('\nCtrl + C is pressed, Lost Connection')
    sys.exit()

#Client prompts input data
try:
    print('\nFill the following information')
    purchase = input('Enter Property Purchase Price: RM ')
    sale = input('\nEnter Property Sale Price: RM ')
    owneryear = input ('\nEnter period of ownership (Year):  ')
    #send list of data JSON to server 
    mydata = {"p": purchase,"s": sale,"o": owneryear}
    sendData = json.dumps(mydata)
    ClientSocket.send(str.encode(sendData)) #send 4
    print("\nData has been sent to the server!")
except KeyboardInterrupt:
    print('\nCtrl + C is pressed, Lost Connection')
    sys.exit()

while True:
    try:
        print("""
                    TAX PROPERTY ONLINE SYSTEM

                    MENU
                    [1] Display the yearly property Taxes
                    [2] Download statement.txt
                    [3] Exit
                                            """)
        option = input('Please enter your options: ') 
        ClientSocket.send(str.encode(option)) #send 6
        if option == '1':
            msg = ClientSocket.recv(SIZE)
            print(msg.decode(FORMAT))
        if option == '2':
            fn = ClientSocket.recv(1024).decode(FORMAT)
            print(f"Receiving the filename.")
            file = open(fn, "w+")
            fd = ClientSocket.recv(1024).decode(FORMAT)
            print(f"Receiving the file data.")
            inbox = ClientSocket.recv(1024).decode(FORMAT)
            print(inbox)
            file.write(fd)
            file.close()
        if option == '3':
            exit = ClientSocket.recv(1024).decode(FORMAT)
            print(exit)
            break
    except KeyboardInterrupt:
        print('\nCtrl + C is pressed, Lost Connection')
        sys.exit()
ClientSocket.close()
