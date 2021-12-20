import RPi.GPIO as GPIO # GPIO 임포트
import time             # time 임포트
 
"""
from selenium import webdriver                                        네이버 스포츠에서 해설 부분을 긁어오는 부분이다
import requests                                                       하지만 실행이 안되는 관계로 주석으로 처리한다....
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

data = [[1, 1, 1, 1, 1, 1, 0],  # 0     4digit 또는 7segment에 숫자를 
        [0, 1, 1, 0, 0, 0, 0],  # 1     표시하기 위한 데이터
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
SEGMENT_PIN = [23,12,18,16,15,4,19]      # segment 핀 설정
for segment in SEGMENT_PIN:
  GPIO.setup(segment, GPIO.OUT)         # 모든 segment 핀들을 아웃풋으로 변경 
  GPIO.output(segment, GPIO.LOW)        # 모든 segment 핀들을 LOW로 설정

DIGIT_PIN = [22,5,24,20]                # digit 핀 설정
for segment in DIGIT_PIN:
  GPIO.setup(segment, GPIO.OUT)         # 모든 digit 핀들을 아웃풋으로 설정
  GPIO.output(segment, GPIO.HIGH)       # 모든 digit 핀들을 HIGH로 설정

def segment_4digit(digit, number):      # 4digit segment를 키기 위한 함수
    for i in range(len(DIGIT_PIN)):   
        if i + 1 == digit:              # 만약 digit 핀이 내가 바꾸고 싶은 digit 핀이라면
            GPIO.output(DIGIT_PIN[i], GPIO.LOW)        # digit 핀을 LOW로 설정
        else:                                          # 만약 digit 핀이 내가 바꾸고 싶은 digit 핀이 아니라면
            GPIO.output(DIGIT_PIN[i], GPIO.HIGH)       # digit 핀을 HIGH로 설정

    for i in range(len(SEGMENT_PIN)):
      GPIO.output(SEGMENT_PIN[i],data[number][i])      # 각 세그먼트 핀들을 내가 원하는 숫자에 대응하는 data 값으로 바꾸기
    time.sleep(0.001)

try:
    f = open("relay.txt","r")           # 해설을 저장해둔 파일을 읽기모드로 열기
    while True:
        relay = f.readline()            # 반복문에서 돌아올 때마다 파일을 한줄 씩 읽기
        if not relay:                   
          break                         # 만약 더이상 읽을 것이 없다면 반복문 나가기     

        # 해설을 내가 원하는 자료로 변환하는 부분
        if len(relay) == 2 or len(relay) == 3 or len(relay) == 5:      # 만약 해설의 길이가 2,3,5일때 = 시간이 나오는 부분일 때

          if len(relay) == 5:                                          # 만약 해설의 길이가 5면 = 추가시간이 나오는 부분이라면 ex) 90+1
            for i in range(len(relay)):                                
              if relay[i] == "+":                                      # 만약 i 가 해설의 + 부분이라면
                change = list(relay)                                   # 해설을 리스트로 바꾸고
                change[i] = '0'                                        # + 부분을 0으로 바꾸고
                relay =''.join(change)                                 # 다시 리스트를 합친다 = int 형으로 변환하기 위함

                                                                       # 해설을 내가 원하는 자료형들로 바꿔놓는다
          t_relay = list(relay)                                        # list 형
          t_relay_char = ''.join(t_relay)                              # char 형
          t_relay_int = int(relay)                                     # int 형


        # 해설을 출력하는 부분
        if len(t_relay_char) == 2 or len(t_relay_char) == 3:           # 해설의 길이가 2, 3이라면 = 추가시간이 아니라면
          if t_relay_int >= 10:                                        # 해설이 두 자리수 이상이라면
            start = time.time()                                        
            while(time.time() - start) <= 1.2:                           # 실행시간이 1초가 되기 전까지 반복한다
              segment_4digit(4,int(t_relay[1]))                        # 4digit의 4번 digit에 10의 자리를 출력한다
              segment_4digit(3,int(t_relay[0]))                        # 4digit의 3번 digit에 1의 자리를 출력한다

          else:                                                        # 해설이 한자리수하면
            start = time.time()                 
            while(time.time() - start) <= 1.2:                           # 실행시간이 1초가 되기 전까지 반복한다.
              segment_4digit(4,int(t_relay[0]))                        # 4digit의 4번 digit에 1의 자리를 출력한다
        elif len(t_relay_char) == 5:                                   # 해설의 길이가 5라면 = 추가시간이라면
              start = time.time()
              while (time.time() - start) <= 1.2:                        # 실행시간이 1초가 되기 전까지 반복한다
                  segment_4digit(1,int(t_relay[0]))                    # 4digit의 1번 digit에 10의 자리를 출력한다
                  segment_4digit(2,int(t_relay[1]))                    # 4digit의 2번 digit에 1의 자리를 출력한다
                  segment_4digit(3,10)                                 # 4digit의 3번 digit에 - 을 출력한다
                  segment_4digit(4,int(t_relay[3]))                    # 4digit의 4번 digit에 추가시간을 출력한다
        
        pass
        print(t_relay_int)

finally:
  GPIO.cleanup()
