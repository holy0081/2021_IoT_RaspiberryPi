from typing_extensions import TypeVarTuple
import RPi.GPIO as GPIO # GPIO 임포트
from lcd import drivers # lcd drivers 임포트
import time             # time 임포트
"""
from selenium import webdriver
import requests
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
 
path = "C:\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(path,chrome_options=options)
driver.implicitly_wait(3)
 
naver_wfootball = "https://m.sports.naver.com/game/2019041850017679872/relay"
driver.get(naver_wfootball)
 
page = driver.page_source
premi_team_rank_list =  BeautifulSoup(page,"html.parser")
team_rank_list = premi_team_rank_list.select('ol.TimeLine_relay_list__31S-r>li')

f = open("C:/programming/raspberrypi/test2/relay.txt","w")
for team in team_rank_list:
    num = team.select('.TimeLine_info__3bhfl>span')[0].text
    relay = team.select('.TimeLine_relay_text_area__3X8le>p')[0].text
    f.write(num+"\n")
    f.write(relay+"\n")

f.close()
"""

GPIO.setmode(GPIO.BCM)  # GPIO.BCM 설정
display = drivers.Lcd() # display 설정

#led
LED_PIN_red = 26        # red led 핀 설정
LED_PIN_blue = 27       # blue led 핀 설정

GPIO.setup(LED_PIN_red, GPIO.OUT)       #red led 출력으로 변경
GPIO.setup(LED_PIN_blue, GPIO.OUT)      #blue led 출력으로 변경

# buzzer
BUZZER_PIN = 5                          #buzzer 핀 설정
GPIO.setup(BUZZER_PIN, GPIO.OUT)        #buzzer 출력으로 변경
pwm = GPIO.PWM(BUZZER_PIN, 262)         
pwm.start(50)                           # 주파수: 도(262Hz)
melody = [392,494]                      # duty cycle

data = [[1, 1, 1, 1, 1, 1, 0],  # 0     4digit 또는 7segment를 표시하기
        [0, 1, 1, 0, 0, 0, 0],  # 1     위한 데이터
        [1, 1, 0, 1, 1, 0, 1],  # 2
        [1, 1, 1, 1, 0, 0, 1],  # 3
        [0, 1, 1, 0, 0, 1, 1],  # 4
        [1, 0, 1, 1, 0, 1, 1],  # 5
        [1, 0, 1, 1, 1, 1, 1],  # 6
        [1, 1, 1, 0, 0, 0, 0],  # 7
        [1, 1, 1, 1, 1, 1, 1],  # 8
        [1, 1, 1, 0, 0, 1, 1],  # 9
        [0, 0, 0, 0, 0, 0, 1]]  # -

SEGMENT_PIN_red = [23,6,18,16,15,4,19]       # red team segment 핀 설정
for segment in SEGMENT_PIN_red:
  GPIO.setup(segment, GPIO.OUT)              # 모든 segment 핀들을 OUT으로 설정
  GPIO.output(segment, GPIO.LOW)             # 모든 segment 핀드를 LOW로 설정

SEGMENT_PIN_blue = [23,6,18,16,15,4,19]      # blue team segment 핀 설정
for segment in SEGMENT_PIN_blue:
  GPIO.setup(segment, GPIO.OUT)              # 모든 segemnt 핀들을 OUT으로 설정
  GPIO.output(segment, GPIO.LOW)             # 모든 segment 핀들을 LOW으로 설정

relay_type = 0                                
goal_m = 0
goal_t = 0
try:
  f = open("relay.txt","r")                  # 해설 파일을 읽기 형식으로 열기
  while True:
    relay = f.readline()                     # 반복문에서 돌아올 때마다 한 줄씩 읽기
    if not relay:
      break                                  # 더이상 해설이 없으면 반복문 나가기

    # 골을 넣었을 시의 효과음이 나오는 부분
    if relay == "GOAL~~!!m\n":                         # 만약 해설이 GOAL~~!!m 이라면
          goal_m = goal_m + 1                          # 맨시티의 골 카운트를 하나 늘린다
          t_relay = relay
          for i in range(len(SEGMENT_PIN_blue)):                                
            GPIO.output(SEGMENT_PIN_blue[i], data[goal_m][i])      # 맨시티 진영의 segment핀들을 골 카운트 숫자가 뜨게 알맞는 data값으로 설정한다
          change = list(relay)                         # 해설을 리스트 형식으로 바꾼다
          change[8] = '        '                       # 해설의 8번째 부분 (m) 을 공백으로 만든다
          relay = ''.join(change)                      # 리스트 형식을 다시 뭉친다
          
    elif relay == "GOAL~~!!t\n":                       # 만약 해설이 GOAL~~!!t 이라면
          goal_t = goal_t + 1                          # 토트넘의 골 카운트를 하나 늘린다
          t_relay = relay
          for i in range(len(SEGMENT_PIN_red)):        
            GPIO.output(SEGMENT_PIN_red[i], data[goal_t][i])        # 토트넘 진영의 segment 핀들을 골 카운트 숫자가 뜨게 알맞는 data 값으로 설정한다
          change = list(relay)                         # 해설을 list 형식으로 바꾼다
          change[8] = '        '                       # 해설의 8번째 부분 (t) 을 공백으로 만든다
          relay = ''.join(change)                      # 리스트 형식을 다시 뭉친다

    # 출력 부분
    if len(relay) != 2 and len(relay) != 3 and len(relay) != 5:     # 해설이 2,3,5글자가 아닐 때 = 숫자 부분이 아닌 글자 부분일 때
          display.lcd_display_string(relay, relay_type)             # display에 해설을 relay_type줄에 쓴다
          if(relay_type == 1):                                
            display.lcd_display_string("                ",2)        # 1번째 줄에 써야 될경우 아랫줄을 지운다

    else:                                                           # 시간 부분일 때
          display.lcd_display_string("                ",1)          #
          display.lcd_display_string("                ",2)          # 디스플레이 화면을 지운다
    
    # 디스플레이 줄 설정 부분
    if len(relay) != 2 and len(relay) != 3 and len(relay) != 5:     # 해설이 시간이 아닐 때
            if relay_type == 1:                                     #                                      
                relay_type = 2                                      # relay_type 이 1이면 2로, 2이면 1로 바꾼다
            else:                                                   # 
                relay_type = 1                                      #
    else:                                                           # 해설이 시간 부분일 때
            relay_type = 1                                          # 해설의 시작부분을 1번째 줄로 고정한다

    if t_relay == "GOAL~~!!m\n":
          GPIO.output(LED_PIN_blue, GPIO.HIGH)         #
          pwm.ChangeFrequency(melody[0])               #
          time.sleep(0.3)                              # 
          GPIO.output(LED_PIN_blue, GPIO.LOW)          # 
          time.sleep(0.1)                              # 
          GPIO.output(LED_PIN_blue, GPIO.HIGH)         # 골을 넣었을 시 효과음을 낸다 
          pwm.ChangeFrequency(melody[0])               # 맨시티 골이면 파란 불을 깜박거리도록 하고
          time.sleep(0.3)                              # 효과음이 나도록 한다
          GPIO.output(LED_PIN_blue, GPIO.LOW)          #
          time.sleep(0.1)                              #
          GPIO.output(LED_PIN_blue, GPIO.HIGH)         #
          pwm.ChangeFrequency(melody[1])               #
          time.sleep(0.2)                              #
          GPIO.output(LED_PIN_blue, GPIO.LOW)          #
    
    elif t_relay == "GOAL~~!!t\n":
          GPIO.output(LED_PIN_red, GPIO.HIGH)          #
          pwm.ChangeFrequency(melody[0])               #
          time.sleep(0.3)                              #
          GPIO.output(LED_PIN_red, GPIO.LOW)           #
          time.sleep(0.1)                              #
          GPIO.output(LED_PIN_red, GPIO.HIGH)          #
          pwm.ChangeFrequency(melody[0])               # 골을 넣었을 시 효과음을 낸다
          time.sleep(0.3)                              # 토트넘 골이라면 빨간 불을 깜박거리도록 하고
          GPIO.output(LED_PIN_red, GPIO.LOW)           # 효과음이 나도록 한다
          time.sleep(0.1)                              #
          GPIO.output(LED_PIN_red, GPIO.HIGH)          #
          pwm.ChangeFrequency(melody[1])               #
          time.sleep(0.2)                              #
          GPIO.output(LED_PIN_red, GPIO.LOW)           #

    else:
      time.sleep(1)                                    # 골 효과음이 나오지 않을 땐 1초 기다린다


finally:
  GPIO.cleanup()
