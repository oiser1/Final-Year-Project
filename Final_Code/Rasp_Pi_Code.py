# Socket object documentation can be found in btmodule.c in bluez folder
# inside PyBluez-0.20. Check bluez.py for implementation of socket object

# Imports serial, time, _thread, csv and bluetooth libraries
import serial
import time
from bluetooth import *
import _thread
import csv
import re

####################### Setup #########################################################
ser = serial.Serial('/dev/ttyAMA0',2000000) # Opens serial port at baud rate of 2000000
ser.flushInput() # Flushes serial input buffer
ser.flushOutput() # Flushes serial output buffer
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
                myLock.release() # Releases lock
            except:
                print("Error1")
        else:
            myPhone_sock.close() # Closes phone's socket (client)
            raspPi_sock.close() # Closes Raspberry Pi's socket (server)
        #print (phoneInstrData) # prints data
    return;
    
def getTrainingData():
    global myError
    while True:
        try:
            myLock.acquire(1,0.01) # Will acquire lock if it can do it in 0.01 seconds
            read_serial1=ser.readline() # Reads data line in from Arduino using RX pin (From sensor 1, left whisker)
            read_serial2=ser.readline() # Reads data line in from Arduino using RX pin (From sensor 2, right whisker)
            myLock.release() # Releases lock
        except:
            print("Error2")
            
        read_serial1 = read_serial1.decode() # Decodes the received byte to string
        read_serial2 = read_serial2.decode() # Decodes the received byte to string
        if ((len(read_serial1) > 4) or (len(read_serial2) > 4)) and (myError == 1):
            read_serial1 = re.sub("[^0-9]", "", read_serial1) # If any letters are present, remove them and leave numbers
            read_serial2 = re.sub("[^0-9]", "", read_serial2)
            myError = 0

        try:
            read_serial1 = int(read_serial1) # converts from string to int
            read_serial2 = int(read_serial2) # converts from string to int
            print (read_serial1)
            print (read_serial2)
                
            #with open('FlatTerrainData.csv', mode='a') as TrainingData:
            #    TrainingDataWriter = csv.writer(TrainingData, delimiter=',')
            #    TrainingDataWriter.writerow([read_serial1,read_serial2])
            #    TrainingData.flush()
                
            #with open('RoughTerrainData.csv', mode='a') as TrainingData:
            #    TrainingDataWriter = csv.writer(TrainingData, delimiter=',')
            #    TrainingDataWriter.writerow([read_serial1,read_serial2])
            #    TrainingData.flush()
                
            #with open('WallData.csv', mode='a') as TrainingData:
            #    TrainingDataWriter = csv.writer(TrainingData, delimiter=',')
            #    TrainingDataWriter.writerow([read_serial1,read_serial2])
            #    TrainingData.flush()
                
            #with open('ObjectTwangData.csv', mode='a') as TrainingData:
            #    TrainingDataWriter = csv.writer(TrainingData, delimiter=',')
            #    TrainingDataWriter.writerow([read_serial1,read_serial2])
            #    TrainingData.flush()
            
        except:
            print("Error3")
                
    return;

def main():
    _thread.start_new_thread(phoneInstr, (myPhone_sock,)) # New thread started for phoneInstr function
    _thread.start_new_thread(getTrainingData,()) # New thread started for getTrainingData function
    while True:
        pass    # Used so program continuosly runs while threads are running

if __name__== "__main__":
  main()
