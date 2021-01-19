from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager

import pyimgur

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(800, 1400)
driver.get("https://tenki.jp/forecast/6/30/")
driver.save_screenshot("screenshot.png")
driver.close()
img = Image.open("screenshot.png")
img.show()
img.crop((20, 367, 710, 930)).save("screenshot2.png")


# CLIENT_ID = 'a2c6f8d4aeca343'
# PATH = "screenshot.png" #A Filepath to an image on your computer"
# title = "Uploaded with PyImgur"

# im = pyimgur.Imgur(CLIENT_ID)
# uploaded_image = im.upload_image(PATH, title=title)
# print(uploaded_image.title)
# print(uploaded_image.link)
# print(uploaded_image.type)