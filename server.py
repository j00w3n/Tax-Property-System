import socket
import sys
import time
import errno
from multiprocessing import Process

ok_message = 'HTTP/1.0 200 OK\n\n'
nok_message = 'HTTP/1.0 404 NotFound\n\n'

def process_start(s_sock):
    s_sock.send(str.encode("\n\nWELCOME TO THE TAX PROPERTY ONLINE SYSTEM"))

def readIC(s_sock):
    ic = s_sock.recv(2048)
    ic = ic.decode("utf-8")
    user_ic = ic[6]+ic[7]
    con_ic = int(user_ic)

    if con_ic <17:
                nation = ("IC:" + str(ic) + "\nWarganegara, you are required to pay 20% of your value rate")
    else:
                nation = ("IC:" + str(ic) + "\nForeigner, you are required to pay 30% of your value rate")
                
    s_sock.send(str.encode(nation))


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
                p2 = Process(target=readIC, args=(s_sock,))

                p1.start()
                p2.start()

                p1.join()
                p2.join()

            except socket.error:
                print('got a socket error')

    except Exception as e:        
        print('an exception occurred!')
        print(e)
        sys.exit(1)
    finally:
     	   s.close()