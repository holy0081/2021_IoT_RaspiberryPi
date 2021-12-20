import RPi.GPIO as GPIO
import time

LPR = 4
LPY = 5
LPG = 6
SPR = 7
SPY = 8
SPG = 9

GPIO.setmode(GPIO.BCM)
GPIO.setup(SPR, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SPY, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SPG, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LPR, GPIO.OUT)
GPIO.setup(LPY, GPIO.OUT)
GPIO.setup(LPG, GPIO.OUT)

try:
  while(1):
    valR = GPIO.input(SPR)
    valY = GPIO.input(SPY)
    valG = GPIO.input(SPG)
    GPIO.output(LPR,valR)
    GPIO.output(LPY,valY)
    GPIO.output(LPG,valG)
    
finally:
  GPIO.cleanup()