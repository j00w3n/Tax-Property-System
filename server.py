#buat line 49 tu dulu , baru commit kat aku balik tau
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
    while True:
        readIC()
        recvAndCal()
        #option() kalau dah siap function ni , uncomment ni atu
    s_sock.close()


def readIC():
    ic = s_sock.recv(2048)
    readIC.ic = ic.decode("utf-8")
    user_ic = ic[6]+ic[7]
    con_ic = int(user_ic)

    if con_ic <17:
                readIC.nation = "citizen"
                answer = ("IC:" + str(readIC.ic) + "\nWarganegara, you are required to pay 20% of your value rate")
                print(f"[+] {s_addr} recognised as Warganegara")
                
    else:
                readIC.nation = "foreigner" 
                answer = ("IC:" + str(readIC.ic) + "\nForeigner, you are required to pay 30% of your value rate")
                print(f"[+] {s_addr} recognised as Foreigner")
                
    s_sock.send(str.encode(answer))

def calc():
    data = s_sock.recv(2048)
    data = json.loads(data.decode())
    purchase = data.get("p")
    calc.buy = int(purchase) #cast value of purchase to int type
    sale = data.get("s")
    calc.sell = int(purchase) #cast value of sale to int type
    owneryear = data.get("o")
    calc.year = int(owneryear) #cast value of owner year to int type
    netCharge = buy - sell # problem kat sini ilyas , dia return 0.0 , kalau aku buat print(buy) , dia keluar value
                            #kalau aku buat print(netCharge) dia retrun 0.0
                            # print aku buat just untuk test je , not a part of program
    print(buy)
    print(f"[+] {s_addr} Data Receive")
    if readIC.nation == "citizen":
        if year < 4:
            calc.taxpay = netCharge * .3
        elif year == 4:
            calc.taxpay = netCharge * .2
        elif year == 5:
            calc.taxpay = netCharge * .15
        else:
            calc.taxpay  = netCharge * .1
    else:
        if year <6:
            calc.taxpay  = netCharge * .3
        else:
            calc.taxpay  = netCharge * .1

    return calc.taxpay 
        
        

"""
def option()
   op = s_sock.recv(2048)
   op = ic.decode("utf-8")
   opt = str(op)
   while opt !=3:
       if opt == '1'

if option == '1':
        a1 = "This is user :" + readIC.ic + "\n"
        a2 = "Your property Purchase Purchase are :" + calc.buy + "\n"
        a3 = "Your property Purchase Sale are :" + calc.sell + "\n"
        a4 = "Your head taxes are :" + "+ calc()\n"
        a5 = "Your yearly property taxes amount :" + "\n"
        mydata = {"p": purchase,"s": sale,"o": owneryear}

        #animated_loading()
        #fetch client info dari server
        #papar amount client perlu bayar
        print("\n")

 elif option == '2':
        f = open("statement.txt","w+")
        f.write("This is user :" + readIC.ic + "\n")
        f.write("Your property Purchase Purchase are :" + calc.buy + "\n")
        f.write("Your property Purchase Sale are :" + calc.sell + "\n")
        f.write("Your head taxes are :" + "+ calc()\n")
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
        """
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