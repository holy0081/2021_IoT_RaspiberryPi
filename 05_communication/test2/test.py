import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

data = [[1, 1, 1, 1, 1, 1, 0],  # 0
        [0, 1, 1, 0, 0, 0, 0],  # 1
        [1, 1, 0, 1, 1, 0, 1],  # 2
        [1, 1, 1, 1, 0, 0, 1],  # 3
        [0, 1, 1, 0, 0, 1, 1],  # 4
        [1, 0, 1, 1, 0, 1, 1],  # 5
        [1, 0, 1, 1, 1, 1, 1],  # 6
        [1, 1, 1, 0, 0, 0, 0],  # 7
        [1, 1, 1, 1, 1, 1, 1],  # 8
        [1, 1, 1, 0, 0, 1, 1],  # 9
        [0, 0, 0, 0, 0, 0, 1]]  # -

#4digit
SEGMENT_PIN = [23,6,18,16,15,4,19]
for segment in SEGMENT_PIN:
  GPIO.setup(segment, GPIO.OUT)
  GPIO.output(segment, GPIO.LOW)

DIGIT_PIN = [22,5,24,20]
for segment in DIGIT_PIN:
  GPIO.setup(segment, GPIO.OUT)
  GPIO.output(segment, GPIO.HIGH)

def segment_4digit(digit, number):
    for i in range(len(DIGIT_PIN)):
        if i + 1 == digit:
            GPIO.output(DIGIT_PIN[i], GPIO.LOW)
        else:
            GPIO.output(DIGIT_PIN[i], GPIO.HIGH)

    for i in range(len(SEGMENT_PIN)):
      GPIO.output(SEGMENT_PIN[i],data[number][i])
    time.sleep(0.001)

try:
  while True:
    segment_4digit(3,9)
    segment_4digit(4,9)

finally:
  GPIO.cleanup()