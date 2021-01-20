from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)
import os
import psycopg2
import pyimgur
from googletrans import Translator

app = Flask(__name__)

line_bot_api = LineBotApi('SoMERI2Dgs8EQsqeiDGUEUVKDDLDOxChkUwvZEMDbaQ8HkgRF8bClo6WoGiE9WXmtUjyZkSN6byabo40k7BEzqpVuGm4JlkWLBQpwdzjPnr5KgiF6ejbfWkuqGHuaPRd8tMU726ErGkxFAjQP/mlrwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('46c74932b451108b7032ec89f7e47f31')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request  body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    msg = event.message.text
    result = word_check(msg)
    if "https" in result:
        image_message = ImageSendMessage(
                            original_content_url=result,
                            preview_image_url=result
                        )
        line_bot_api.reply_message(event.reply_token, image_message)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result))

def word_check(message):

    if "天気" in message or "天氣" in message :
        return weather()
    elif message[:2] == "@日":
        return translate_text(message[2:],dest='ja')
    elif message[:2] == "@中":
        return translate_text(message[2:],dest='zh-tw')
    elif message[:2] == "@英":
        return translate_text(message[2:],dest='en')
    elif message[:2] == "@韓": 
        return translate_text(message[2:],dest='ko')
    else:
        return database_word(message)

def translate_text(text,dest='en'):

    translator = Translator()
    result = translator.translate(text, dest).text
    return result

def weather():

    img_url = "https://smtgvs.weathernews.jp/s/forecast/img25/KINKI_today.png"
    return img_url

def database_word(message):
    conn = psycopg2.connect(database="d5l1ehhk24qmdk",
                            user="jglgvqhikukisk",
                            password="285f7a822763e5ae8730a2910c20e4ebbd9954506cc5a4a8b4281729410cc719",
                            host="ec2-3-216-181-219.compute-1.amazonaws.com",
                            port="5432")
    cursor = conn.cursor()

    if "學一下" in message:

        learn = message.split("!")
        cursor.execute("INSERT INTO word(word_id,user_word,bot_word,created_on) VALUES(DEFAULT,'" + learn[1].strip() + "','" + learn[2].strip() + "','2021-01-02')")
        bot_word = "已學會新語言!!" + learn[2].strip()

    else:

        cursor.execute("SELECT user_word, bot_word FROM word;")
        data = []
        while True:
            temp = cursor.fetchone()
            if temp:
                data.append(temp)
            else:
                break
                
        for d in data:
            if d[0] in message:
                bot_word = d[1]

    conn.commit()
    cursor.close()
    conn.close()

    return bot_word


if __name__ == "__main__":
    app.run()