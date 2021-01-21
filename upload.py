import requests as rq
from bs4 import BeautifulSoup
import json,urllib.request
import time

data_url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-A5FB0E56-1660-4D54-BC65-6D3D6F14D376&format=JSON"
img_url = "https://www.cwb.gov.tw/V8/C/W/OBS_Temp.html"
map_url = "https://www.cwb.gov.tw"
time = int(time.strftime("%H", time.localtime()))
r = rq.get(img_url)
if r.status_code == rq.codes.ok:
    soup = BeautifulSoup(r.text, "html.parser")
    mapr = soup.find("img", class_="img-responsive").get("src")
 
full_url = map_url + mapr[:-4] + "w" + mapr[-4:]

with urllib.request.urlopen(data_url) as url:
    word = []
    data = json.loads(url.read().decode())
    if time >= 0 and time < 12:
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
    say += "\n"
    for i in w:
        say += i
        say += "\n"
result = [full_url, say]
if "https://www.cwb.gov.tw" in  result[0]:
    print("a")
