from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(800, 1400)
driver.get("https://tenki.jp/forecast/6/30/")
driver.save_screenshot("screenshot.png")
driver.close()
img = Image.open("screenshot.png")
img.crop((20, 367, 710, 930)).save("screenshot.png")

