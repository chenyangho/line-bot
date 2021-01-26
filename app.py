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
        FlexMessage = json.load(open('creator.json','r',encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                            alt_text='Creator',
                            contents=FlexMessage
                        ))

    elif result[1] == "food":
        FlexMessage = json.load(open('food.json','r',encoding='utf-8'))

        for i in range(3): 
            # url
            FlexMessage['contents'][i]['hero']['url'] = result[0][i][0]
            # shop_name
            FlexMessage['contents'][i]['body']['contents'][0]['text'] = result[0][i][1]
            # address
            FlexMessage['contents'][i]['body']['contents'][1]['contents'][0]['contents'][0]['text'] = result[0][i][2]
            # action
            FlexMessage['contents'][i]['hero']['action']['uri'] = result[0][i][3]

        line_bot_api.reply_message(event.reply_token, FlexSendMessage(
                            alt_text='Food',
                            contents=FlexMessage
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
    elif "レストラン" in message or "ランチ" in message or "ラーメン" in message or "スイーツ" in message:
        return (food(message), "food")
    else:
        return database_word(message)
    

def food(message):

    url = "https://tabelog.com/osaka/A2701/A270101/"
    r = rq.get(url)
    img_url = []
    res_name = []
    address = []
    result = []
    action_url = []
    if r.status_code == rq.codes.ok:
        soup = BeautifulSoup(r.text, "html.parser")
        top_three = soup.find_all("li", class_="areatop-top3__rst-item")
        for shop in top_three:
            a = shop.find("div", class_="areatop-top3__rst-img")
            # image_url
            image_url = a.select_one("img").get("src")
            img_url.append(image_url)
            # shop_name
            shop_name = a.find("h3").getText()
            res_name.append(shop_name)
            # address & type
            address_type = a.find("span", class_="areatop-top3__area-catg").getText().replace(' ','').replace('\n','')
            address.append(address_type)
            action = shop.find("a", class_="areatop-top3__rst-target").get('href')
            action_url.append(action)

    if "レストラン" in message:
        result.extend([(img_url[0], res_name[0], address[0], action_url[0]),(img_url[1], res_name[1], address[1], action_url[1]),(img_url[2], res_name[2], address[2], action_url[2])])
    elif "ランチ" in message:
        result.extend([(img_url[3], res_name[3], address[3], action_url[3]),(img_url[4], res_name[4], address[4], action_url[4]),(img_url[5], res_name[5], address[5], action_url[5])])
    elif "ラーメン" in message: 
        result.extend([(img_url[6], res_name[6], address[6], action_url[6]),(img_url[7], res_name[7], address[7], action_url[7]),(img_url[8], res_name[8], address[8], action_url[8])])
    elif "スイーツ" in message:
        result.extend([(img_url[9], res_name[9], address[9], action_url[9]),(img_url[10], res_name[10], address[10], action_url[10]),(img_url[11], res_name[11], address[11], action_url[11])])

    return result


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

    if "學一下" in message[:3]:

        learn = message.split("!")
        cursor.execute("INSERT INTO word(word_id,user_word,bot_word,created_on) VALUES(DEFAULT,'" + learn[1].strip() + "','" + learn[2].strip() + "','2021-01-02')")
        bot_word = "已學會新語言!!" + learn[2].strip()

    elif "何が話せる" in message:

        cursor.execute("SELECT user_word, bot_word FROM word;")
        data = []
        learned = ""
        while True:
            temp = cursor.fetchone()
            if temp:
                data.append(temp)
            else:
                break

        for word in data:
            learned += word[0] + "-->" + word[1] + "\n"

        return learned

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