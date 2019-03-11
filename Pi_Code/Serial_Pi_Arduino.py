# Imports serial and time libraries
import serial
import time

ser = serial.Serial('/dev/ttyAMA0',9600) # Opens serial port

# continuous loop
while True:
	print ("Hello there!")					# prints to screen
	#ser.write ('General Kenobi!!'.encode())	# writes to serial TX and encodes it		
	read_serial=ser.readline()				# reads line from serial RX
	print (read_serial)						# prints what it has read from RX to screen
	time.sleep(1)							# pauses for 1 second

# Following is some code which would use a class to implement the serial communication
# but I couldn't get it to work successfully

#class SerialWrapper:
#	def __init__(self, device):
#		self.ser = serial.Serial(device, 9600)

#	def sendData(self, data):
#		data += "\r\n"
#		self.ser.write(data.encode('utf-8'))
        
#	def readData(self, n):
#		self.ser.read()

#def main():
#	ser = SerialWrapper('/dev/ttyAMA0')
#	n = 10
#	while True:
#		print ('Hello there!')
#		data = ('General Kenobi!')
#		ser.sendData(data)
#		read_serial = ser.readData(n)
#		print (read_serial)
#		time.sleep(1)
        
#while True:
#	main()

