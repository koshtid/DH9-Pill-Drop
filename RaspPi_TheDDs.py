#import every class in gpiozero library
from gpiozero import *

#time stuff
import time
from time import sleep
from datetime import datetime

#set up pins for Button and LED
button = Button(21)

'''MAKE SURE TO HAVE MATPLOTLIB DOWNLOADED'''
##import libraries for graph
import numpy as np
import matplotlib.pyplot as plt

'''TWILIO'''
import sys
import random
import os
from twilio.rest import Client#imports library that allows me to text a phone number via sms
account_sid = "AC91e75a4205d2294db0a84c6489ddce47"#variables needed for the sms text function 
auth_token = "b5b3b1babc9b5241db497775b11558b5"
client = Client(account_sid, auth_token) #initializes things



#DHANDHAN CODE
from smbus import SMBus
 
addr = 0x8 # bus address, binary code  1000000
bus = SMBus(1) # indicates /dev/ic2-1


#PATIENT MEDICATION RECORD
drug0 = "zara"
drug1 = "weanne"
drug2 = "dhandhan"

med0= False
med1= False
med2 = False

schedule0 = ["11:08:00","09:51:00"]
schedule1 = ["11:08:00","12:30:00","15:30:00","18:30:00", "21:30:00", "00:30:00"]
schedule2 = ["11:08:00","12:30:00","18:30:00"]

def taken():
    counter = 0
    while counter != 15:
        if button.is_pressed:
            print("Pill Taken")
            print("TIME\tMEDICINE\tDOSAGE\tTAKEN\n")
            return "Yes"
        else:
            counter+=1
            print(counter)
            time.sleep(1)
    print("TIME\tMEDICINE\tDOSAGE\tTAKEN\n")
    return "No"
##
##def dispense():
##    while True:
##        now = datetime.now()
##        current_time = now.strftime("%H:%M:%S")
##
##        if current_time in schedule0:
##                #dispense medicine from dhandhan's code twice
##                bus.write_byte_data(addr, 0x00, 1) # send int 1 to the arduino, motor 1
##                time.sleep(1)
##                bus.write_byte_data(addr, 0x00, 1) # send int 1 to the arduino, motor 1
##
##        if current_time in schedule1:
##                #dispense medicine from dhandhan's code
##                bus.write_byte_data(addr, 0x00, 2) # send int 2 to the arduino, motor 1
##
##
##        if current_time in schedule2:
##                #dispense medicine from dhandhan's code
##                bus.write_byte_data(addr, 0x00, 3) # send int 3 to the arduino, motor 1
##
##        
##        #wait to see
##        response = taken()
##        if med0 == True:
##            data_file(current_time,drug0,"2", response)
##        if med1 == True:
##            data_file(current_time,drug1,"1", response)
##        if med2 == True:
##            data_file(current_time,drug2,"1", response)



def dispense():
    addr = 0x8 # bus address, binary code  1000000
    bus = SMBus(1) # indicates /dev/ic2-1

    dropped0 = False
    dropped1 = False
    dropped2 = False

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if current_time in schedule0:
            #dispense medicine from dhandhan's code twice
            bus.write_byte_data(addr, 0x00, 1) # send int 1 to the arduino, motor 1
            bus.write_byte_data(addr, 0x00, 4)
            dropped0 = True

        if current_time in schedule1:
            #dispense medicine from dhandhan's code
            bus.write_byte_data(addr, 0x00, 2) # send int 2 to the arduino, motor 1
            bus.write_byte_data(addr, 0x00, 4)
            dropped1 = True
            
        if current_time in schedule2:
            #dispense medicine from dhandhan's code
            bus.write_byte_data(addr, 0x00, 3) # send int 3 to the arduino, motor 1
            bus.write_byte_data(addr, 0x00, 4)
            dropped2 = True

        if(dropped0 == True or dropped1 == True or dropped2 ==True):
            break

    #wait to see
    response = taken()
    if dropped0 == True:
        data_file(current_time,drug0,"1", response)
    if dropped1 == True:
        data_file(current_time,drug1,"1", response)
    if dropped2 == True:
        data_file(current_time,drug2,"1", response)

      
def twilio():
  print("Texting Doctor Patient Information") #inform the user the code has called the emergency number
  text=['Date & Time: '+str(datetime.now()) + 'PATIENT_DRUGdata.txt']#creates a list that contains everything included within the sms text message 
  client.messages.create(to="+16478071442", from_ = "+12162902513", body = text)#sends the sms text message to the presaved number


#write data to file"
def data_file(time,name,dosage,response):

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
      
    file = open("PATIENT_DRUGdata.txt", 'a')
  
    #current data point is put in a list with corresponding avereage, responses, time, etc.
    all_data = [time,name,dosage,response]

    #list of data is converted into string 
    data = '\t\t'.join([str(item) for item in all_data])

    #data is written onto the text file
    file.write(data+'\n')
    file.close()

    #data is printed onto shell 
    print(data)

    answer = input("Send Data to Physician? (y/n)\n")
    counter = 0
    
    while counter != 7:
        if answer == "y":
            twilio()
            break
        else:
            counter +=1
            timer.sleep(1)
    break


def main():
  #initialize txtfile; erase old data from txtfile
  file = open("PATIENT_DRUGdata.txt", 'w')
  file.write("TIME \tMEDICINE \tDOSAGE \tTAKEN\n")
  file.close()
  
  print("When ready, press the button to start the sensor!\nPress again when you're done using the sensor!")
  
  #to activate the dispenser
  button.wait_for_press()
  
  print("TIME\tMEDICINE\tDOSAGE\tTAKEN\n")

  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")

  print(current_time)
  
  dispense()

##CALL MAIN FUNCTION
main()
