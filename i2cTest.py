#  Raspberry Pi Master for Arduino Slave
#  i2c_master_pi.py
#  Connects to Arduino via I2C
  
#  DroneBot Workshop 2019
#  https://dronebotworkshop.com
from smbus import SMBus
 
addr = 0x8 # bus address, binary code  1000000
bus = SMBus(1) # indicates /dev/ic2-1

def dispenserControl():
     
    print ("Enter 1 for motor 1, 2 for motor 2, or 3 for motor 3")
    flag = 1

    while flag == 1: 

        servoChoice = int(input(">>>>   "))
     
        if servoChoice == 1:
            bus.write_byte_data(0x8, 0x00, 1) # send int 1 to the arduino, motor 1
            flag = 0
        elif servoChoice == 2:
            bus.write_byte_data(0x8, 0x00, 2) # send int 2 to the arduino, motor 2
            flag = 0
        elif servoChoice == 3:
            bus.write_byte_data(0x8, 0x00, 3) # send int 3 to the arduino, motor 3
            flag = 0
        elif servoChoice == 4:
            bus.write_byte_data(0x8, 0x00, 4) # send int 4 to the arduino, buzzer
            flag = 0

def receiveSignal():
    data = bus.read_byte(0x7)
    print(data)

while True:
    #receiveSignal()
    dispenserControl()
