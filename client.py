import sys
import socket
import os
import time

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

#Response = ClientSocket.recv(1024)
#print(Response.decode('utf-8'))
#cResp = "Client 1 is connected to the server!"
#ClientSocket.send(str.encode(cResp))
welcome = ClientSocket.recv(2048)
print(welcome.decode("utf-8"))

input_ic = input('Please enter your Identity Card: ')
ClientSocket.send(str.encode(input_ic))
ResponseIC=ClientSocket.recv(2048)
print(ResponseIC.decode("utf-8"))


#prop_val = input('Please enter your Property Value: ')
#address = input('Please enter your Address: ')
#owneryear = input ('Please enter period of ownership: ')


print("""
                 MENU
                 [1] Yearly property taxes
                 [2] Print out statement
                 [3] Exit
                                         """)

option = ''
while option != '3':

 option = input('Please enter your options: ')

 if option == '1':
        #Client1socket.send(str.encode(option)) #send client info ke server
        animated_loading()
        #fetch client info dari server
        #papar amount client perlu bayar
        print("\n")

 elif option == '2':
        f = open("statement.txt","w+")
        f.write("This is user :" + ic + "\n")
        f.write("Your property taxes are :" + prop_val + "\n")
        f.write("Your head taxes are :" + "\n")
        f.write("Your yearly property taxes amount :" + "\n")
        animated_loading()
        print("Statement has been saved successfully! Please check your folder.")
        print("\n")

 elif option == '3':
        print("Closing connection")
        sys.exit()
        ClientSocket.close()
        f.close()
 else:
        print("Input not recognised")
