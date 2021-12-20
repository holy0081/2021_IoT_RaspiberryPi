import RPi.GPIO as GPIO
import time

SERVO_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(7.5)

try:
  while True:
    val = input('1: 0도, 2: -90도, 3:90도, 9:exit >')
    if val  == '1':
      pwm.ChangeDudyCycle(7.5)
    elif val == '2':
      pwm.ChangeDudyCycle(5)
    elif val == '3':
      pwm.ChangeDudyCycle(10)
    elif val == '9':
      break

finally:
  pwm.stop()
  GPIO.cleanup()

  
