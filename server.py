import socket
import sys
from time import ctime
import time
import errno
from multiprocessing import Process
import json
import os
import signal
from termcolor import colored #pip install termcolor
from pyfiglet import Figlet #pip install pyfiglet

ok_message = 'HTTP/1.0 200 OK\n\n'
nok_message = 'HTTP/1.0 404 NotFound\n\n'

FORMAT = 'utf-8'

def process_start(s_sock):
    #BANNER
    try:
        s_sock.send(str.encode('\n\nWELCOME TO THE TAX PROPERTY ONLINE SYSTEM'))
        f = Figlet(font='standard')
        banner = colored(f.renderText('PROPERTY TAX ONLINE'), 'green')
        s_sock.send(str.encode(banner))
        #BANNER
        readIC()
        calc()
        while True:
            option()
    except KeyboardInterrupt:
        print('\nCtrl + C is pressed, Lost Connection')
        sys.exit()

def animated_loading():
    anime = ['.']
    done = False
    while done is False:
        for i in anime:
            print(f'[+] {s_addr} Please wait while system is Loading...')
            time.sleep(0.5)
            done = True

def animated_generate():
    anime = ['.']
    done = False
    while done is False:
        for i in anime:
            print(f'[+] {s_addr} Generating statement.txt file')
            time.sleep(0.5)
            done = True
    
def animated_calc():
    anime = ['.']
    done = False
    while done is False:
        for i in anime:
            print(f'[+] {s_addr} Calculating...')
            time.sleep(0.5)
            done = True

def readIC():
    ic = s_sock.recv(2048) 
    readIC.ic = ic.decode(FORMAT)
    try:
        user_ic = readIC.ic[6]+readIC.ic[7]
        con_ic = int(user_ic)
        if con_ic < 17:
            readIC.nation = 'Malaysian'
            answer = ('IC:' + str(readIC.ic) + '\nNationality : '+ readIC.nation)
            print(f'[+] {s_addr} Recognised as ',readIC.nation)            
        else:
            readIC.nation = 'Foreigner' 
            answer = ('IC:' + str(ic) + '\nationality : '+ readIC.nation)
            print(f'[+] {s_addr} Recognised as ',readIC.nation)
        s_sock.send(str.encode(answer)) 
    except IndexError:
        print("No IC input")

def calc():
    data = s_sock.recv(2048) #recv 4
    try:
        data = json.loads(data.decode())
        purchase = data.get('p')
        calc.buy = int(purchase) #cast value of purchase to int type
        sale = data.get('s')
        calc.sell = int(sale) #cast value of sale to int type
        owneryear = data.get('o')
        calc.year = int(owneryear) #cast value of owner calc.year to int type
        netCharge = calc.sell - calc.buy 
        animated_loading()
        print(f'[+] {s_addr} Data Received')
        animated_calc()

        if readIC.nation == 'citizen':
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

        print(f'[+] {s_addr} Calculation Done')
    except json.decoder.JSONDecodeError:
        print('No JSON data from clinet')


def option():
    try:
        print(f"[+] {s_addr} Waiting for client's option...")
        op = s_sock.recv(2048) #recv 6
        op = op.decode(FORMAT)
        opt = str(op)
        
        if opt == '1':
                print(f'[+] {s_addr} Client pick option '+ opt + ': Yearly Property Taxes')
                msg =('User :' + str(readIC.ic) + 
                    '\nYour property Purchase Purchase are :' + str(calc.buy) + 
                    '\nYour property Purchase Sale are :' + str(calc.sell) + 
                    '\nYour Period of Ownership :' + str(calc.year) + 
                    '\nYour Yearly Property Taxes Amount :' + str(calc.taxpay) + '\n')
                s_sock.send(str.encode(msg))
                print(f'[+] {s_addr} Data has been displayed to the client')
        
        elif opt == '2':
                print(f'[+] {s_addr} Client pick option '+ opt + ': Print out Statement')
                f = open('statement.txt','x')
                f.write('YEARLY PROPERTY TAX\n\n')
                f.write('User :' + str(readIC.ic) + '\nYour property purchase are : RM ' + str(calc.buy) + '\nYour Property Sale are : RM ' + str(calc.sell) +'\nPeriod of ownership : ' + str(calc.year)+ ' years\nYour yearly property taxes amount : RM' + str(calc.taxpay)+'\n')
                f.close()
                f = open('statement.txt','r')
                data = f.read()
                s_sock.send('statement.txt'.encode(FORMAT))
                s_sock.send(data.encode(FORMAT))
                animated_generate()      
                print(f'[+] {s_addr} Statement has been sent to the client')
                inbox = "Please check your inbox"
                s_sock.send(inbox.encode(FORMAT))
                f.close()
                os.remove('statement.txt')
                
        else:
            exit = 'Thank you for using Property Tax Online'
            s_sock.send(str.encode(exit))
            print(f'[+] {s_addr} Client Disconnected')
            sys.exit()
    except Exception:
        print("No Option Selected")
    
if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',8888))
    print('Listening . . .')
    s.listen(3)
    try:
        while True:
            try:
                s_sock, s_addr = s.accept()
                f = open ('database.txt','a')
                print(f'[+] {s_addr} Connected')
                f.write('\nClient Connected :')
                f.write(f'[+] {s_addr} \nTimeStamp : ' + ctime())
                f.close()
                p1 = Process(target=process_start, args=(s_sock,))
                p1.start()
            except socket.error:
                print('got a socket error')
    except KeyboardInterrupt:
        print('\nCtrl + C is pressed, Server Close')
        sys.exit()
    except Exception as e:        
        print('an exception occurred!')
        print(e)
        sys.exit(1)
    finally:
     	s.close()
