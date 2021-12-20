from flask import Flask, render_template
import RPi.GPIO as GPIO

LED_PIN = 22
GPIO.setmode(GPIO.BCM) # GPIO.BCM or GPIO.BOARD
GPIO.setup(LED_PIN, GPIO.OUT)

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("led2.html")

@app.route("/led/<op>")
def led_op(op):
  if op == "on":
    GPIO.output(LED_PIN, 1)
    return "LED ON"

  elif op == "off":
    GPIO.output(LED_PIN, 0)
    return "LED OFF"
  
  else:
    return "ERROR"

#터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
  try:
    app.run(host="0.0.0.0")
  finally:
    GPIO.cleanup()