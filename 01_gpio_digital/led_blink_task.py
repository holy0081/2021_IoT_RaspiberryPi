import RPi.GPIO as GPIO
import time

LED_PIN_red = 4
LED_PIN_yellow = 5
LED_PIN_green = 6

GPIO.setmode(GPIO.BCM) # GPIO.BCM or GPIO.BOARD
GPIO.setup(LED_PIN_red, GPIO.OUT)
GPIO.setup(LED_PIN_yellow, GPIO.OUT)
GPIO.setup(LED_PIN_green, GPIO.OUT)

GPIO.output(LED_PIN_red, 1)
time.sleep(2)
GPIO.output(LED_PIN_red, 0)
time.sleep(2)

GPIO.output(LED_PIN_yellow, 1)
time.sleep(2)
GPIO.output(LED_PIN_yellow, 0)
time.sleep(2)

GPIO.output(LED_PIN_green, 1)
time.sleep(2)
GPIO.output(LED_PIN_green, 0)
time.sleep(2)

GPIO.cleanup() 