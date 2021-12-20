import RPi.GPIO as GPIO
#from lcd import drivers
import time

GPIO.setmode(GPIO.BCM)
#display = drivers.Lcd()

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

DIGIT_PIN = [22,5,6,20]
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

relay_type = 1
time_type = 1
goal_t = 0
goal_m = 0
a = 0
try:
    f = open("relay.txt","r")
    while True:
        relay = f.readline()
        if not relay:
          break

        if relay == "GOAL~~!!m\n":
          goal_m = goal_m + 1
          change = list(relay)
          change[8] = '        ' 
          relay = ''.join(change)

        elif relay == "GOAL~~!!t\n":
          goal_t = goal_t + 1
          change = list(relay)
          change[8] = '        ' 
          relay = ''.join(change)    

        print(relay)
        """
        if len(relay) != 2 and len(relay) != 3 and len(relay) != 5:
          display.lcd_display_string(relay, relay_type)
          if(relay_type == 1):
            display.lcd_display_string("                ",2)

        else:
          display.lcd_display_string("                ",1)
          display.lcd_display_string("                ",2)

        if len(relay) != 2 and len(relay) != 3 and len(relay) != 5:
            if relay_type == 1:
                relay_type = 2
            else:
                relay_type = 1
        else:
            relay_type = 1
        """
        if len(relay) == 2 or len(relay) == 3 or len(relay) == 5:

          if len(relay) == 5:
            for i in range(len(relay)):
              if relay[i] == "+":
                change = list(relay)
                change[i] = '0'
                relay =''.join(change)

          t_relay = list(relay)
          t_relay_char = ''.join(t_relay)
          t_relay_int = int(relay)

        if len(t_relay_char) == 2 or len(t_relay_char) == 3:
          if t_relay_int >= 10:
            start = time.time()
            while(time.time() - start) <= 1:
              segment_4digit(3,int(t_relay[0]))
              segment_4digit(4,int(t_relay[1]))
              

          else:
            start = time.time()
            while(time.time() - start) <= 1:
              segment_4digit(4,int(t_relay[0]))
        else:
              start = time.time()
              while (time.time() - start) <= 1:
                  segment_4digit(1,int(t_relay[0]))
                  segment_4digit(2,int(t_relay[1]))
                  segment_4digit(3,10)
                  segment_4digit(4,int(t_relay[3]))
        
        pass

finally:
  GPIO.cleanup()