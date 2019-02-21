import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)

while True:
    GPIO.output(40, 1)
    GPIO.output(38, 0)
    GPIO.output(36, 0)
    time.sleep(5)
    GPIO.output(40, 0)
    GPIO.output(38, 1)
    GPIO.output(36, 0)
    time.sleep(2)
    GPIO.output(40, 0)
    GPIO.output(38, 0)
    GPIO.output(36, 1)
    time.sleep(5)
