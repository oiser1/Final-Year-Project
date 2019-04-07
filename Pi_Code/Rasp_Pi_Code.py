# Socket object documentation can be found in btmodule.c in bluez folder
# inside PyBluez-0.20. Check bluez.py for implementation of socket object

# Imports serial, time and bluetooth libraries
import serial
import time
from bluetooth import *
import _thread
import csv
#import bluetooth

####################### Setup #########################################################
ser = serial.Serial('/dev/ttyAMA0',9600) # Opens serial port at baud rate of 9600

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
        else:
            myPhone_sock.close() # Closes phone's socket (client)
            raspPi_sock.close() # Closes Raspberry Pi's socket (server)
    return;
    
def getTrainingData():
    while True:
        read_serial=ser.readline() # Reads data line in from Arduino uisng RX pin
        read_serial = read_serial.rstrip()
        print (read_serial)
        with open('TrainingData.csv', mode='w', newline='') as TrainingData:
            TrainingDataWriter = csv.writer(TrainingData)
            TrainingDataWriter.writerow(read_serial)
    return;

def main():
    _thread.start_new_thread(phoneInstr, (myPhone_sock,))
    _thread.start_new_thread(getTrainingData,())

    while True:
        pass

if __name__== "__main__":
  main()
