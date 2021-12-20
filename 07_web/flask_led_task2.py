from flask import Flask, render_template
import RPi.GPIO as GPIO

RED_LED_PIN = 22
YELLOW_LED_PIN = 4
GPIO.setmode(GPIO.BCM) # GPIO.BCM or GPIO.BOARD
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("led2.html")

@app.route("/led/<op>")
def led_op(op):
  if op == "redon":
    GPIO.output(RED_LED_PIN, 1)
    return "RED LED ON"

  elif op == "redoff":
    GPIO.output(RED_LED_PIN, 0)
    return "RED LED OFF"

  elif op == "yellowon":
    GPIO.output(YELLOW_LED_PIN, 1)
    return "YELLOW LED ON"

  elif op == "yellowoff":
    GPIO.output(YELLOW_LED_PIN, 0)
    return "YELLOW LED OFF"

  else:
    return "ERROR"

#터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
  try:
    app.run(host="0.0.0.0")
  finally:
    GPIO.cleanup()