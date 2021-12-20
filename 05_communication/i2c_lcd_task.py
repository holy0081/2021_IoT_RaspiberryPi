from lcd import drivers
import time
import datetime
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
display = drivers.Lcd()
PIN = 4

try:
  while True:
   h,t = Adafruit_DHT.read_retry(sensor, PIN)
   if h is not None and t is not None:
     display.lcd_display_string(f"{t:.1f}C, {h:.1f}%", 2)
   now = datetime.datetime.now()
   display.lcd_display_string(now.strftime("%x%X"), 1)
   
finally:
  display.lcd_clear()