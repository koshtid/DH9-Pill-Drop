
#import every class in gpiozero library
from gpiozero import *

#time stuff
import time
from time import sleep
from datetime import datetime

start_time = time.time()


#set up pins for Button and LED
button = Button(21)

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

##schedule0 = ["12:06:30","09:51:00"]
##schedule1 = ["12:06:30","12:30:00","15:30:00","18:30:00", "21:30:00", "00:30:00"]
##schedule2 = ["12:06:30","12:30:00","18:30:00"]

def taken():
    counter = 0
    while counter != 5:
        if button.is_pressed:
            print("Pill Taken")
            print("TIME \t\t\tMEDICINE \tDOSAGE \t\tTAKEN\n")
            return "Yes"
        else:
            counter+=1
            print(counter)
            time.sleep(1)
    print("TIME \t\t\tMEDICINE \tDOSAGE \t\tTAKEN\n")
    return "No"


def elapsed(start_time):
    now_time = time.time()
    return (now_time - start_time)


def dispense():
    addr = 0x8 # bus address, binary code  1000000
    bus = SMBus(1) # indicates /dev/ic2-1

    dropped0 = False
    dropped1 = False
    dropped2 = False

    start_time0 = time.time()
    start_time1 = time.time()
    start_time2 = time.time()

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        if elapsed(start_time0) >= random.randint(1,9):
            #dispense medicine from dhandhan's code twice
            bus.write_byte_data(addr, 0x00, 1) # send int 1 to the arduino, motor 1
            bus.write_byte_data(addr, 0x00, 4)
            dropped0 = True
            start_time0 = time.time()
        if elapsed(start_time1) >= random.randint(1,9):
            #dispense medicine from dhandhan's code
            bus.write_byte_data(addr, 0x00, 2) # send int 2 to the arduino, motor 1
            bus.write_byte_data(addr, 0x00, 4)
            dropped1 = True
            start_time1 = time.time()
        if elapsed(start_time2) >= random.randint(1,9):
            #dispense medicine from dhandhan's code
            bus.write_byte_data(addr, 0x00, 3) # send int 3 to the arduino, motor 1
            bus.write_byte_data(addr, 0x00, 4)
            dropped2 = True
            start_time2 = time.time()
        sleep(0.1)

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
    now = datetime.now()
    print("Texting Doctor Patient Information") #inform the user the code has called the emergency number
    text=['\nDate & Time: '+ now.strftime("%H:%M:%S") + '\nPATIENT_DRUGdata.txt']#creates a list that contains everything included within the sms text message
    client.messages.create(to="+16478071442", from_ = "+12162902513", body = text)#sends the sms text message to the presaved number
    print("Done!")
    
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
        if answer == "y" or answer == "Y":
            twilio()
            break
        elif answer == "n" or answer == "N":
            print("Sure!")
            break
        else:
            counter +=1
            time.sleep(1)
        break

def main():
  #initialize txtfile; erase old data from txtfile
  file = open("PATIENT_DRUGdata.txt", 'w')
  file.write("TIME \t\t\tMEDICINE \tDOSAGE \t\tTAKEN\n")
  file.close()

  flag = 0
  print("When ready, press the button to start the Pill Drop!\n")
  
  #to activate the dispenser
  button.wait_for_press()
  
  while flag == 0:
      
      now = datetime.now()
      current_time = now.strftime("%H:%M:%S")

      print(current_time)
      
      dispense()

      time.sleep(3)

      print("Press the Button in the next 5s if you would like to quit")
      for i in range(5):
          print(i+1)
          if button.is_pressed:
              exit(0)
          time.sleep(1)

      

##CALL MAIN FUNCTION
main()
