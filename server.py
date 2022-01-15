import socket
import sys
import time
import errno
from multiprocessing import Process
import json
import math

ok_message = 'HTTP/1.0 200 OK\n\n'
nok_message = 'HTTP/1.0 404 NotFound\n\n'

def process_start(s_sock):
    s_sock.send(str.encode("\n\nWELCOME TO THE TAX PROPERTY ONLINE SYSTEM"))
    readIC()
    calc()
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
    ic = s_sock.recv(2048)
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
                
    s_sock.send(str.encode(answer))

def calc():
    data = s_sock.recv(2048)
    data = json.loads(data.decode())
    
    purchase = data.get("p")
    calc.buy = int(purchase) #cast value of purchase to int type
    sale = data.get("s")
    calc.sell = int(sale) #cast value of sale to int type
    owneryear = data.get("o")
    calc.year = int(owneryear) #cast value of owner calc.year to int type
    netCharge = calc.sell - calc.buy 
    animated_loading()
    print(f"[+] {s_addr} Data Receive")
    print(f"[+] {s_addr} Making Calculation")

    #if netCharge < 0:
        #s_sock.send(str.encode(replyCharge))
        
    
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
    s_sock.send(str.encode("""
                 MENU
                 [1] Yearly property taxes
                 [2] Print out statement
                 [3] Exit
                                         """))
    op = s_sock.recv(2048)
    op = op.decode("utf-8")
    opt = str(op)
    if opt == '1':
            msg =("User :" + str(readIC.ic) + 
                "\nYour property Purchase Purchase are :" + str(calc.buy) + 
                "\nYour property Purchase Sale are :" + str(calc.sell) + 
                "\nYour Period of Ownership :" + str(calc.sell) + 
                "\nYour Yearly Property Taxes Amount :" + str(calc.taxpay) + "\n")
            s_sock.send(str.encode(msg))
        

    elif opt == '3':
            print("Closing connection")
            sys.exit()
            ClientSocket.close()
            f.close()
    else:
            print("Input not recognised")

#buat macam mana nak create file dekat server , and send ke client

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",8888))
    print("listening...")
    s.listen(3)
    
    try:
        while True:
            try:
                s_sock, s_addr = s.accept()
                nation =""
                print(f"[+] {s_addr} connected")
                p1 = Process(target=process_start, args=(s_sock,))
                p1.start()
                p1.join()
                

            except socket.error:
                print('got a socket error')

    except Exception as e:        
        print('an exception occurred!')
        print(e)
        sys.exit(1)
    finally:
     	   s.close()