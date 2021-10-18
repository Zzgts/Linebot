from __future__ import unicode_literals
from threading import stack_size
from flask import Flask,render_template,request,abort
import selenium
app=Flask(__name__)
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextMessage,TextSendMessage,MessageAction, messages

import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time

line_bot_api = LineBotApi('line_bot_api')
handler = WebhookHandler('your webhook handler')
#路徑
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/callback",methods=['POST'])
def callback() :
    signature= request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try :
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

if __name__ == '__main__' :
    app.run()
