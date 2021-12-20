from flask import Flask
import RPi.GPIO as GPIO

LED_PIN = 22
GPIO.setmode(GPIO.BCM) # GPIO.BCM or GPIO.BOARD
GPIO.setup(LED_PIN, GPIO.OUT)

app = Flask(__name__)

@app.route("/")
def led():
  return '''
  <p>Hello, Flask!</p>
  <a href="/led/on">LED ON</a>
  <a href="/led/off">LED OFF</a>
  '''

@app.route("/led/<op>")
def led_op(op):
  if op == "on":
    GPIO.output(LED_PIN, 1)
    return '''
    <p>LED ON</p>
    <a href="/">Go home</a>
    '''

  if op == "off":
    GPIO.output(LED_PIN, 0)
    return '''
    <p>LED OFF</p>
    <a href="/">Go home</a>
    '''

#터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
  try:
    app.run(host="0.0.0.0")
  finally:
    GPIO.cleanup()