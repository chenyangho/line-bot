import requests as rq
from bs4 import BeautifulSoup

url = "https://weathernews.jp/onebox/tenki/kinki/"
img_url = "https://smtgvs.weathernews.jp/s/forecast/img25/KINKI_today.png"
r = rq.get(url)
if r.status_code == rq.codes.ok:
    soup = BeautifulSoup(r.text, "html.parser")
    city = soup.find("h1").getText()
    
    print(city)