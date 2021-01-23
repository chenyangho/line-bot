from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage
)
import os
import psycopg2
import pyimgur
from googletrans import Translator
import requests as rq
from bs4 import BeautifulSoup
import json
import urllib
import time

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
    profile = line_bot_api.get_profile(event.source.user_id)
    msg = event.message.text
    result = word_check(msg)
    if "https://smtgvs." in result:
        image_message = ImageSendMessage(
                            original_content_url=result,
                            preview_image_url=result
                        )
        line_bot_api.reply_message(event.reply_token, image_message)

    elif "https://www.cwb.gov.tw" in result[0]:
        image_message = ImageSendMessage(
                            original_content_url=result[0],
                            preview_image_url=result[0]
                        )

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result[1]))

        line_bot_api.push_message(profile.user_id, image_message)

    elif result == "flex_message":
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                            alt_text='hello',
                            contents={'type': 'bubble','hero': {'type': 'image','url': 'https://i.imgur.com/4hng01H.jpg','size': 'full'},'body': {'type': 'box','layout': 'vertical','contents': [{'type': 'text','text': '陳暘和','color': '#487e95','weight': 'bold','style': 'normal','decoration': 'none','position': 'relative','size': 'xl'},{'type': 'box','layout': 'vertical','contents': [{'type': 'text','text': 'ECCコンピューター専門学校　在学','size': 'sm'}]},{'type': 'box','layout': 'baseline','contents': [{'type': 'icon','url': 'https://www.flaticon.com/svg/vstatic/svg/941/941565.svg?token=exp=1611393042~hmac=b1c4644da87587d8bf41510c6d395c35','size': 'xl','offsetTop': 'lg'},{'type': 'text','text': 'jacky85031085@gmail.com','margin': 'md','offsetTop': 'sm'}],'paddingAll': 'none'}]}}
                        ))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result))
        
# 輸入判定
def word_check(message):

    if message[:2] == "@日":
        return translate_text(message[2:],dest='ja')
    elif message[:2] == "@中":
        return translate_text(message[2:],dest='zh-tw')
    elif message[:2] == "@英":
        return translate_text(message[2:],dest='en')
    elif message[:2] == "@韓": 
        return translate_text(message[2:],dest='ko')
    elif "天氣" in message:
        return weather_taiwan()
    elif "天気" in message:
        return weather_japan()
    elif "Show creator" in message:
        return "flex_message"
    else:
        return database_word(message)
    

# 翻譯功能
def translate_text(text,dest='en'):

    translator = Translator()
    result = translator.translate(text, dest).text
    return result

# 查天氣功能(japan)
def weather_japan():

    img_url = "https://smtgvs.weathernews.jp/s/forecast/img25/KINKI_today.png"
    return img_url

# 查天氣功能(taiwan)
def weather_taiwan():
    data_url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-A5FB0E56-1660-4D54-BC65-6D3D6F14D376&format=JSON"
    img_url = "https://www.cwb.gov.tw/V8/C/W/OBS_Temp.html"
    map_url = "https://www.cwb.gov.tw"

    r = rq.get(img_url)
    if r.status_code == rq.codes.ok:
        soup = BeautifulSoup(r.text, "html.parser")
        map_img = soup.find("img", class_="img-responsive").get("src")
    last_url = map_url + map_img[:-4] + "w" + map_img[-4:]

    hour = int(time.strftime("%H", time.localtime())) - 9
    with urllib.request.urlopen(data_url) as url:
        word = []
        data = json.loads(url.read().decode())
        if hour >= 0 and hour < 12:
            now = 0
            word.append(["上午"])
        else:
            now = 1
            word.append(["下午"])
        for i in range(22):
            # 城市名子
            city = data['cwbopendata']['dataset']['location'][i]['locationName']
            # 天氣概況
            about = "天氣概況 : " + data['cwbopendata']['dataset']['location'][i]['weatherElement'][0]['time'][now]['parameter']['parameterName']
            # 最高氣溫
            MAXt = "最高氣溫 : " + data['cwbopendata']['dataset']['location'][i]['weatherElement'][1]['time'][now]['parameter']['parameterName'] + "°C"
            # 最低氣溫
            MINt = "最低氣溫 : " + data['cwbopendata']['dataset']['location'][i]['weatherElement'][2]['time'][now]['parameter']['parameterName'] + "°C"
            # 降雨機率
            PoP = "降雨機率 : " + data['cwbopendata']['dataset']['location'][i]['weatherElement'][4]['time'][now]['parameter']['parameterName'] + "%"
            word += [[city, about, MAXt, MINt, PoP]]

    say = ""
    for w in word:
        for i in w:
            say += i
            say += "\n"
        say += "\n"

    result_weather = [last_url, str(say)]

    return result_weather


# 學/回話
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