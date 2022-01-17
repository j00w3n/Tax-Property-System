import socket
import sys
import time
import errno
from multiprocessing import Process
import json
import os
from termcolor import colored #pip install termcolor
from pyfiglet import Figlet #pip install pyfiglet


ok_message = 'HTTP/1.0 200 OK\n\n'
nok_message = 'HTTP/1.0 404 NotFound\n\n'

def process_start(s_sock):
    #BANNER
    s_sock.send(str.encode("\n\nWELCOME TO THE TAX PROPERTY ONLINE SYSTEM"))
    f = Figlet(font='standard')
    banner = colored(f.renderText('TAX ONLINE'), 'green')
    s_sock.send(str.encode(banner))
    #BANNER
    readIC()
    calc()
    while True:
        option() 
    s_sock.close()

def animated_loading():

 anime = [".",".","."]

 done = False

 while done is False:
      for i in anime:
       print(f'[+] {s_addr} Please wait while system is Loading...')
       time.sleep(0.5)
       done = True

def readIC():
    ic = s_sock.recv(2048) #recv 2
    readIC.ic = ic.decode("utf-8")
    user_ic = readIC.ic[6]+readIC.ic[7]
    con_ic = int(user_ic)
    con_ic = 0
    if con_ic <17:
                readIC.nation = "citizen"
                answer = ("IC:" + str(readIC.ic) + "\nStatus : Warganegara \nYou are required to pay 20% of your value rate")
                print(f"[+] {s_addr} Recognised as Warganegara")
                
    else:
                readIC.nation = "foreigner" 
                answer = ("IC:" + str(readIC.ic) + "\nStatus : Foreigner \nYou are required to pay 30% of your value rate")
                print(f"[+] {s_addr} Recognised as Foreigner")
                
    s_sock.send(str.encode(answer)) #send 3

def calc():
    data = s_sock.recv(2048) #recv 4
    data = json.loads(data.decode())
    purchase = data.get("p")
    calc.buy = int(purchase) #cast value of purchase to int type
    sale = data.get("s")
    calc.sell = int(sale) #cast value of sale to int type
    owneryear = data.get("o")
    calc.year = int(owneryear) #cast value of owner calc.year to int type
    netCharge = calc.sell - calc.buy 
    animated_loading()
    print(f"[+] {s_addr} Data Receive") #ni shuk contoh
    print(f"[+] {s_addr} Making Calculation")

    if readIC.nation == "citizen":
        if calc.year < 4:
            calc.taxpay = netCharge * .3
        elif calc.year == 4:
            calc.taxpay = netCharge * .2
        elif calc.year == 5:
            calc.taxpay = netCharge * .15
        else:
            calc.taxpay  = netCharge * .1
    else:
        if calc.year <6:
            calc.taxpay  = netCharge * .3
        else:
            calc.taxpay  = netCharge * .1

    print(f"[+] {s_addr} Calculation Done")


def option():
    op = s_sock.recv(2048) #recv 6
    op = op.decode("utf-8")
    opt = str(op)
    if opt == '1':
            msg =("User :" + str(readIC.ic) + 
                "\nYour property Purchase Purchase are :" + str(calc.buy) + 
                "\nYour property Purchase Sale are :" + str(calc.sell) + 
                "\nYour Period of Ownership :" + str(calc.sell) + 
                "\nYour Yearly Property Taxes Amount :" + str(calc.taxpay) + "\n")
            s_sock.send(str.encode(msg))
            print(f"[+] {s_addr} Data has been displayed to the client")
    
    elif opt == '2':
            f = open("statement.txt","x")
            f.write("User :" + str(readIC.ic) + "\nYour property purchase are :" + str(calc.buy) + "\nYour Property Sale are :" + str(calc.sell) + "\nYour yearly property taxes amount :" + str(calc.taxpay) +"\nPeriod of ownership : " + str(calc.year))
            f.close()
            f = open("statement.txt","r")
            data = f.read()
            s_sock.send("statement.txt".encode("utf-8"))
            s_sock.send(data.encode("utf-8"))
            f.close()
            os.remove("statement.txt")
            print(f"[+] {s_addr} Statement has been sent to the client")

    
if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",8888))
    print("listening...")
    s.listen(3)
    try:
        while True:
            try:
                s_sock, s_addr = s.accept()
                print(f"[+] {s_addr} connected")
                p1 = Process(target=process_start, args=(s_sock,))
                p1.start()
            except socket.error:
                print('got a socket error')

    except Exception as e:        
        print('an exception occurred!')
        print(e)
        sys.exit(1)
    finally:
     	   s.close()
