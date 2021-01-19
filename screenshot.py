from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager

import pyimgur

# 螢幕截圖
# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.set_window_size(800, 1400)
# driver.get("https://tenki.jp/forecast/6/30/")
# driver.save_screenshot("screenshot.png")
# driver.close()
# img = Image.open("screenshot.png")
# img.show()
# img.crop((20, 367, 710, 930)).save("screenshot2.png")

# 上傳圖片到imgur圖床
# imgur token，方便日後減少pin使用
# client = ImgurClient(client_id, client_secret, access_token, refresh_token)
# client_id = 'a2c6f8d4aeca343'
# client_secret = 'e3783d13b65005986d60685c98676c02f9ac30c2'
# access_token = "2e69d8f02e65bd23c5515c17d9d293df8f860444"
# refresh_token = "139e700c88335f8215120ff3f3edd83b0e4f6a70"

# CLIENT_ID = 'a2c6f8d4aeca343'
# PATH = "screenshot.png" #A Filepath to an image on your computer"
# title = "Uploaded with PyImgur"

# im = pyimgur.Imgur(CLIENT_ID)
# uploaded_image = im.upload_image(PATH, title=title)
# print(uploaded_image.title)
# print(uploaded_image.link)
# print(uploaded_image.type)


message = "hello"
if "天気" in message  or "天氣" in message :
    print(2)
# elif "教えるよ！" or "羊我教你！":
#     return word_learn()
else:
    print(1)