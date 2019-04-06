# Socket object documentation can be found in btmodule.c in bluez folder
# inside PyBluez-0.20. Check bluez.py for implementation of socket object

# Imports serial, time and bluetooth libraries
#import serial
#import time

from bluetooth import *
#import bluetooth
#ser = serial.Serial('/dev/ttyAMA0',9600) # Opens serial port

raspPi_sock=BluetoothSocket(RFCOMM) # Opens bluetooth socket of RFCOMM protocol
raspPi_sock.bind(("",PORT_ANY)) # Binds socket to a local address and uses any available port
raspPi_sock.listen(1) # Starts listening for one incoming connection and will refuse any others

port = raspPi_sock.getsockname()[1] # returns port being used

#uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

#advertise_service( raspPi_sock, "RaspberryPi",
#                   service_id = uuid,
#                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
#                   profiles = [ SERIAL_PORT_PROFILE ])

print ("Waiting for connection on RFCOMM channel %d" % port)

myPhone_sock, myPhone_addr = raspPi_sock.accept() # Accepts a connection, returns client socket and address
print ("Accepted connection from ", myPhone_addr)

try:
    while True:
        data = myPhone_sock.recv(8) # receives up to 8 bytes from socket, stores in data
        if len(data) == 0: break
        print ("received [%s]" % data) # prints data
except IOError:
    pass

print ("disconnected")

myPhone_sock.close() # Closes phone's socket (client)
raspPi_sock.close() # Closes Raspberry Pi's socket (server)
