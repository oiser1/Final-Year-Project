import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

GPIO.output(37, 1)
GPIO.output(8, 1)
while True:
    # Drive forward
    GPIO.output(40, 1)
    GPIO.output(38, 0)
    GPIO.output(10, 1)
    GPIO.output(12, 0)

    time.sleep(5)
    # Drive backward
    #GPIO.output(40, 0)
    #GPIO.output(38, 1)
    #GPIO.output(10, 0)
    #GPIO.output(12, 1)

    time.sleep(5)
    # Stop
    #GPIO.output(40, 0)
    #GPIO.output(38, 0)
    #GPIO.output(10, 0)
    #GPIO.output(12, 0)
    #time.sleep(5)
