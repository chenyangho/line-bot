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
from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
import os
import psycopg2
import pyimgur

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
                            original_content_url=result ,
                            preview_image_url=result
                        )
        result = image_message

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result))

def word_check(message):

    if "天気" or "天氣" in message:
        return weather()
    # elif "教えるよ！" or "羊我教你！":
    #     return word_learn()
    else:
        return database_word(message)


def weather():

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_size(800, 1400)
    driver.get("https://tenki.jp/forecast/6/30/")
    driver.save_screenshot("screenshot.png")

    img = Image.open("screenshot.png")
    img.crop((20, 367, 710, 930)).save("screenshot.png")

    CLIENT_ID = 'a2c6f8d4aeca343'
    PATH = "screenshot.png" #A Filepath to an image on your computer"
    title = "Uploaded with PyImgur"

    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    driver.close()

    return uploaded_image.link


def database_word(message):
    conn = psycopg2.connect(database="d5l1ehhk24qmdk",
                            user="jglgvqhikukisk",
                            password="285f7a822763e5ae8730a2910c20e4ebbd9954506cc5a4a8b4281729410cc719",
                            host="ec2-3-216-181-219.compute-1.amazonaws.com",
                            port="5432")
    cursor = conn.cursor()
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