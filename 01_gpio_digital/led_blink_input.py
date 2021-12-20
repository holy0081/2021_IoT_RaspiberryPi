import RPi.GPIO as GPIO

LED_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
  while True:
    val = input("1 : On, 0 : Off, 9 : Exit > ")

    if val == '0':
      GPIO.output(LED_PIN, GPIO.LOW)
      print("Led Off\n")

    elif val == '1':
      GPIO.output(LED_PIN, GPIO.HIGH)
      print("Led On\n")

    elif val == '9':
      break

finally:
  GPIO.cleanup()
  print("cleanup and exit")






















