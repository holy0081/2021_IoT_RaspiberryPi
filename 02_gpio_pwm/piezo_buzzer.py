# 도 출력하기

import RPi.GPIO as GPIO
import time

BUZZER_PIN = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# 주파수: 도(262Hz)
pwm = GPIO.PWM(BUZZER_PIN, 262)
pwm.start(10) # duty cycle

try:
  time.sleep(2)
  pwm.ChangeDutyCycle(0)

finally:
  pwm.stop()
  GPIO.cleanup()
