# from selenium import webdriver
# from PIL import Image
# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.set_window_size(800, 1400)
# driver.get("https://tenki.jp/forecast/6/30/")
# driver.save_screenshot("screenshot.png")
# driver.close()
# img = Image.open("screenshot.png")
# img.crop((20, 367, 710, 930)).save("screenshot.png")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

# ブラウザーを起動
options = Options()
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Google検索画面にアクセス
driver.get('https://www.google.co.jp/')

# htmlを取得・表示
html = driver.page_source
print(html)

# ブラウザーを終了
driver.quit()