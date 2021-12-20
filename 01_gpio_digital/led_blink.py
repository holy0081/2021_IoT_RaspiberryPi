import RPi.GPIO as GPIO
import time

LED_PIN = 7
GPIO.setmode(GPIO.BCM) # GPIO.BCM or GPIO.BOARD
GPIO.setup(LED_PIN, GPIO.OUT)

for i in range(10):
  GPIO.output(LED_PIN, 1)
  print("led on")
  time.sleep(1)

  GPIO.output(LED_PIN, 0)
  print("led off")
  time.sleep(1)

GPIO.cleanup() 

