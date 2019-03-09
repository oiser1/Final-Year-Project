import RPi.GPIO as GPIO
import lcd
lcd.lcd_init()
# set cursor to line 1
lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
# display text centered on line 1
lcd.lcd_string("This is my", 2)
# set cursor to line 2
lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
# display additional text on line 2
lcd.lcd_string("LCD display", 2)
#lcd.GPIO.cleanup()
