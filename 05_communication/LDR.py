import spidev
import time
import RPi.GPIO as GPIO

LED_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# SPI 인스턴스 생성
spi = spidev.SpiDev()

# SPI 통신 시작
spi.open(0, 0) # bus:0, dev:0 (CE0, CE1)

# SPI 통신 최대 속도 설정
spi.max_speed_hz = 1000000

# 0~7까지 채널에서 SPI 데이터 읽기
def analog_read(channel):
  ret = spi.xfer2([1, (channel + 8) << 4, 0])
  adc_out = ((ret[1] & 3) << 8) + ret[2]
  return adc_out

try:
  while True:
    reading = analog_read(0) # 0 ~ 1023
    # 전압수치값 변환(0 ~ 3.3V)
    voltage = reading * 3.3/1023
    print("REading = %d, VOltage = %f" % (reading,voltage))
    if reading > 512:
      GPIO.output(LED_PIN, GPIO.HIGH)
    else:
      GPIO.output(LED_PIN, GPIO.LOW)

finally:
  GPIO.cleanup()
  spi.close()