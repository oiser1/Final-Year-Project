# Socket object documentation can be found in btmodule.c in bluez folder
# inside PyBluez-0.20. Check bluez.py for implementation of socket object

# Imports the following libraries
import serial
import time
from bluetooth import *
import _thread
import csv
import re
import tensorflow as tf
from tensorflow import keras
import RPi.GPIO as GPIO
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

global graph,model
graph = tf.get_default_graph()

robotModel = tf.keras.models.load_model('MLRobot.h5')
####################### Setup #########################################################
RST = None     # on the PiOLED this pin isnt used
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()
    
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
    return;

def getData():
    global myError
    #error = 0
    leftWhiskArr = np.array([])
    rightWhiskArr = np.array([])
    numSamples = 0
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

        leftWhiskArr = np.append(leftWhiskArr,read_serial1)
        rightWhiskArr = np.append(rightWhiskArr, read_serial2)
        #numSamples=numSamples+1
        
        if (len(leftWhiskArr) == 50):
            print("Hello1")
            leftWhiskResult=deployNN(leftWhiskArr)
            rightWhiskResult=deployNN(rightWhiskArr)
            displayNNResult(leftWhiskResult,rightWhiskResult)
            #numSamples = 0
            leftWhiskArr = np.array([])
            rightWhiskArr = np.array([])
            print("Hello4")
            
                

    return;

def displayNNResult(leftWhiskResult, rightWhiskResult):
    print("Hello3.1")
    

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # 
    if (leftWhiskResult == 0):
        leftWhiskString = 'Flat Terrain'
    elif (leftWhiskResult == 1):
        leftWhiskString = 'Rough Terrain'
    elif (leftWhiskResult == 2):
        leftWhiskString = 'Wall'
    else:
        leftWhiskString = 'Object Twang'
        
    if (rightWhiskResult == 0):
        rightWhiskString = 'Flat Terrain'
    elif (rightWhiskResult == 1):
        rightWhiskString = 'Rough Terrain'
    elif (rightWhiskResult == 2):
        rightWhiskString = 'Wall'
    else:
        rightWhiskString = 'Object Twang'

    draw.text((x, top),       "Left Whisker: ",  font=font, fill=255)
    draw.text((x, top+8),       leftWhiskString,  font=font, fill=255)
    draw.text((x, top+24),       "Right Whisker: ",  font=font, fill=255)
    draw.text((x, top+32),       rightWhiskString,  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    print("Hello3.2")
    return;

def deployNN(whiskData):
    #whiskData = (whiskData - whiskData.min())/(whiskData.max() - whiskData.min()) # Normalises data
    print("Hello2.1")
    whiskData = np.expand_dims(whiskData, axis=0)
    print("Hello2.2")
    with graph.as_default():
        prediction = robotModel.predict(whiskData)
    result = np.argmax(prediction)
    #result = np.argmax(robotModel.predict(whiskData))
    print(result)
    
    return result;

def main():
    _thread.start_new_thread(phoneInstr, (myPhone_sock,)) # New thread started for phoneInstr function
    _thread.start_new_thread(getData,()) # New thread started for getData function
    #_thread.start_new_thread(displayNNResult,())
    while True:
        pass    # Used so program continuosly runs while threads are running

if __name__== "__main__":
  main()
