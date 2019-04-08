# Socket object documentation can be found in btmodule.c in bluez folder
# inside PyBluez-0.20. Check bluez.py for implementation of socket object

# Imports serial, time, _thread, csv and bluetooth libraries
import serial
import time
from bluetooth import *
import _thread
import csv
#import bluetooth

####################### Setup #########################################################
ser = serial.Serial('/dev/ttyAMA0',9600) # Opens serial port at baud rate of 9600
ser.flushInput()
ser.flushOutput()

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
    while True:
        phoneInstrData = myPhone_sock.recv(8) # receives up to 8 bytes from socket, stores in phoneInstrData
        if len(phoneInstrData) != 0:
            print (phoneInstrData) # prints data
            ser.write(phoneInstrData) # Sends data to Arduino over Tx pin
            ser.flushOutput()
            ser.flushInput()
        else:
            myPhone_sock.close() # Closes phone's socket (client)
            raspPi_sock.close() # Closes Raspberry Pi's socket (server)
        #print (phoneInstrData) # prints data
        #ser.write(phoneInstrData) # Sends data to Arduino over Tx pin
    return;
    
def getTrainingData():
    while True:
        read_serial1=ser.readline() # Reads data line in from Arduino using RX pin (From sensor 1)
        read_serial2=ser.readline() # Reads data line in from Arduino using RX pin (From sensor 2)
        read_serial1 = read_serial1.decode() # Decodes the received byte to string
        read_serial2 = read_serial2.decode() # Decodes the received byte to string
        read_serial1 = int(read_serial1) # converts from string to int
        read_serial2 = int(read_serial2) # converts from string to int
        print (read_serial1)
        print (read_serial2)
        # Opens csv file, ready for appending to. Appends sensor 1 and 2 data values 
        # to the csv file. Flushes the files buffer.
        with open('TrainingData.csv', mode='a') as TrainingData:
            TrainingDataWriter = csv.writer(TrainingData, delimiter=',')
            TrainingDataWriter.writerow([read_serial1,read_serial2])
            TrainingData.flush()
    return;

def main():
    _thread.start_new_thread(phoneInstr, (myPhone_sock,)) # New thread started for phoneInstr function
    _thread.start_new_thread(getTrainingData,()) # New thread started for getTrainingData function
    while True:
        pass    # Used so program continuosly runs while threads are running

if __name__== "__main__":
  main()
