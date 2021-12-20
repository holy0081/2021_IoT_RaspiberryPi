from flask import Flask
import RPi.GPIO as GPIO

LED_RED_PIN = 22
LED_YELLOW_PIN = 23
GPIO.setmode(GPIO.BCM) # GPIO.BCM or GPIO.BOARD
GPIO.setup(LED_RED_PIN, GPIO.OUT)
GPIO.setup(LED_YELLOW_PIN, GPIO.OUT)

app = Flask(__name__)

@app.route("/")
def led():
  return '''
  <p>Hello, Flask!</p>
  <p><a href="/led/red/on">RED LED ON</a>
  <a href="/led/red/off">RED LED OFF</a></p>
  <p><a href="/led/yellow/on">YELLOW LED ON</a>
  <a href="/led/yellow/off">YELLOW LED OFF</a></p>
  '''

@app.route("/led/<ry>/<op>")
def led_op(ry,op):
  if ry == "red":
    if op == "on":
      GPIO.output(LED_RED_PIN, 1)
      return '''
      <p>RED LED ON</p>
      <a href="/">Go home</a>
      '''

    if op == "off":
      GPIO.output(LED_RED_PIN, 0)
      return '''
      <p>RED LED OFF</p>
      <a href="/">Go home</a>
      '''
  if ry == "yellow":
    if op == "on":
      GPIO.output(LED_YELLOW_PIN, 1)
      return '''
      <p>YELLOW LED ON</p>
      <a href="/">Go home</a>
      '''

    if op == "off":
      GPIO.output(LED_YELLOW_PIN, 0)
      return '''
      <p>YELLOW LED OFF</p>
      <a href="/">Go home</a>
      '''

#터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
  try:
    app.run(host="0.0.0.0")
  finally:
    GPIO.cleanup()