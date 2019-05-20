# Socket object documentation can be found in btmodule.c in bluez folder
# inside PyBluez-0.20. Check bluez.py for implementation of socket object

# Imports serial, time, _thread, csv and bluetooth libraries
import serial
import time
from bluetooth import *
import _thread
#import threading
import csv
import re
#import bluetooth
import RPi.GPIO as GPIO
import lcd
import numpy as np
####################### Setup #########################################################
ser = serial.Serial('/dev/ttyAMA0',2000000) # Opens serial port at baud rate of 2000000
ser.flushInput()
ser.flushOutput()
myError = 0
myLock = _thread.allocate_lock()
raspPi_sock=BluetoothSocket(RFCOMM) # Opens bluetooth socket of RFCOMM protocol
raspPi_sock.bind(("",PORT_ANY)) # Binds socket to a local address and uses any available port
raspPi_sock.listen(1) # Starts listening for 1 incoming connection and will refuse any others
port = raspPi_sock.getsockname()[1] # returns port being used

print ("Waiting for connection on RFCOMM channel %d" % port)

# Will sit here until a bluetooth connection is made
# Accepts a connection, returns client socket and address
myPhone_sock, myPhone_addr = raspPi_sock.accept()
print ("Accepted connection from ", myPhone_addr)
############################################################################################

#class phoneThread(threading.Thread):
#    def __init__(self, threadID, name, myPhone_sock):
#        threading.Thread.__init__(self)
#        self.threadID = threadID
#        self.name = name
#        self.myPhone_sock = myPhone_sock
#    def run(self):
#        threadLock.acquire()
#        phoneInstr(myPhone_sock)
#    
def phoneInstr(myPhone_sock):
    global myError
    while True:
        phoneInstrData = myPhone_sock.recv(10) # receives up to 10 bytes from socket, stores in phoneInstrData
        if len(phoneInstrData) != 0:
            print (phoneInstrData) # prints data
            try:
                myLock.acquire(1,0.01) # Will acquire lock if it can do it in 0.01 seconds
                ser.write(phoneInstrData) # Sends data to Arduino over Tx pin
                myError = 1
                #ser.flushOutput()
                #ser.flushInput()
                myLock.release()
            except:
                print("Error1")
        else:
            myPhone_sock.close() # Closes phone's socket (client)
            raspPi_sock.close() # Closes Raspberry Pi's socket (server)
        #print (phoneInstrData) # prints data
        #ser.write(phoneInstrData) # Sends data to Arduino over Tx pin
    return
    
def getData():
    global myError
    #error = 0
    leftWhiskArr = np.array([])
    rightWhiskArr = np.array([])
    countFlag = 0
    while True:
        try:
            myLock.acquire(1,0.01) # Will acquire lock if it can do it in 0.01 seconds
            read_serial1=ser.readline() # Reads data line in from Arduino using RX pin (From sensor 1)
            read_serial2=ser.readline() # Reads data line in from Arduino using RX pin (From sensor 2)
            myLock.release()
        except:
            print("Error2")
            #error = 1
            
        read_serial1 = read_serial1.decode() # Decodes the received byte to string
        read_serial2 = read_serial2.decode() # Decodes the received byte to string
        if ((len(read_serial1) > 4) or (len(read_serial2) > 4)) and (myError == 1):
            read_serial1 = re.sub("[^0-9]", "", read_serial1) # If any letters are present, remove them and leave numbers
            read_serial2 = re.sub("[^0-9]", "", read_serial2)
            myError = 0
            
        try:
            read_serial1 = int(read_serial1) # converts from string to int
            read_serial2 = int(read_serial2) # converts from string to int
            read_serial1 = read_serial1/1023
            read_serial2 = read_serial2/1023
            print (read_serial1)
            print (read_serial2)
        except:
            print("Error3")

        L0Weights = np.load("Layer0Weights.npy")
        L0Biases = np.load("Layer0Biases.npy")
        L1Weights = np.load("Layer1Weights.npy")
        L1Biases = np.load("Layer1Biases.npy")
        L2Weights = np.load("Layer2Weights.npy")
        L2Biases = np.load("Layer2Biases.npy")

        #if (countFlag == 0):
        #    leftWhiskArr = np.append(leftWhiskArr,read_serial1)
        #    rightWhiskArr = np.append(rightWhiskArr, read_serial2)
            if (len(leftWhiskArr == 50)):
                inputs = leftWhiskArr
                weights = L0Weights
                Biases = L0Biases

    return

def displayNNResult(leftWhiskOut, rightWhiskOut):
    lcd.lcd_init()
    # set cursor to line 1
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    # display text centered on line 1
    lcd.lcd_string("Left whisker:", 2)
    # set cursor to line 2
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    # display text centered on line 2
    lcd.lcd_string(leftWhiskOut, 2)

    # set cursor to line 4
    lcd.lcd_byte(lcd.LCD_LINE_4, lcd.LCD_CMD)
    # display additional text on line 4
    lcd.lcd_string("Right whisker:", 2)
    # set cursor to line 5
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    # display text centered on line 5
    lcd.lcd_string(rightWhiskOut, 2)

def deployNN():
    L0Weights = np.load("Layer0Weights.npy")
    L0Biases = np.load("Layer0Biases.npy")
    L1Weights = np.load("Layer1Weights.npy")
    L1Biases = np.load("Layer1Biases.npy")
    L2Weights = np.load("Layer2Weights.npy")
    L2Biases = np.load("Layer2Biases.npy")


def main():
    _thread.start_new_thread(phoneInstr, (myPhone_sock,)) # New thread started for phoneInstr function
    _thread.start_new_thread(getData,()) # New thread started for getData function
    #_thread.start_new_thread(displayNNResult,())
    while True:
        pass    # Used so program continuosly runs while threads are running

if __name__== "__main__":
  main()
