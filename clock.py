from __future__ import unicode_literals
import configparser
from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
import datetime
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextMessage,TextSendMessage,MessageAction, messages
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
sched = BlockingScheduler()

enable=False      #判斷第一次傳送開/關台 資訊
line_bot_api = LineBotApi('line_bot_api')
handler = WebhookHandler('your webhookhandler')
to ='dst linechat handler'

title=" "
status="offline"
#網頁抓取資料
def get():
    global title,status
    options = Options()
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN',None)
    options.add_argument("--disable-notifications")
    options.add_argument("--headless") #無頭模式
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver =webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH",None),chrome_options=options)
    driver.get('https://www.twitch.tv/alenwu666')
    try :
        status=driver.find_element_by_xpath("//p[@class='sc-AxirZ gOlXkb']").get_attribute('innerHTML')
        if status=="LIVE"and enable==False:
            title=driver.find_element_by_xpath("//h2[@class='sc-AxirZ cUlgmo']").get_attribute('innerHTML')
#sc-AxirZ ktnnZK
    except NoSuchElementException:
        status="offline"
    driver.close()

def nostream():
    global status,enable,title
    if status=="LIVE"and enable==False:
        line_bot_api.push_message(to, TextSendMessage(text='streaming now \n '+title+'\n'+'啊丁開台了快點來掛台摟 https://www.twitch.tv/alenwu666 '))
        print("開台")
        enable=True


    elif status!="LIVE"and enable==True:
        line_bot_api.push_message(to, TextSendMessage(text='offline 休息摟 下..下次一定開到死'))
        print("關台")
        enable=False



@sched.scheduled_job('interval', minutes=20)
def scheduled_job():
    # print('========== APScheduler CRON =========')
    # print('This job runs every weekday */2 min.')
    # print('========== APScheduler CRON =========')

    url = "https://twitchbotzz.herokuapp.com/"
    conn = urllib.request.urlopen(url)

    for key, value in conn.getheaders():
        print(key, value)

#時間
@sched.scheduled_job('interval', seconds=90)
def scheduled():
    print("HI")
    get()
    nostream()
    print("end")
    

sched.start()

