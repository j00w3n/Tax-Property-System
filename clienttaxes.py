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

input_ic = input('Please enter your Identity Card: ')
ic = input_ic
user_ic = ic[6]+ic[7]
con_ic = int(user_ic)
os.system('clear')

if con_ic < 17:
            print('IC: ', ic)
            print('Warganegara, you are required to pay 20% of your value rate')
            prop_val = input('Please enter your Property Value: ')
            address = input('Please enter your Address: ')
            owneryear = input ('Please enter period of ownership: ')
else:
            print('IC: ', ic)
            print('Foreigner, you are required to pay 30% of your value rate')
            prop_val = int(input('Please enter your Property Value: '))
            address = input('Please enter your Address: ')
            owneryear = int(input ('Please enter period of ownership: '))

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
        f.close()
 else:
        print("Input not recognised")
