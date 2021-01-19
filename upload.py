#取得token，方便日後減少pin使用
#client = ImgurClient(client_id, client_secret, access_token, refresh_token)
# client_id = 'a2c6f8d4aeca343'
# client_secret = 'e3783d13b65005986d60685c98676c02f9ac30c2'
# access_token = "2e69d8f02e65bd23c5515c17d9d293df8f860444"
# refresh_token = "139e700c88335f8215120ff3f3edd83b0e4f6a70"

import pyimgur

CLIENT_ID = 'a2c6f8d4aeca343'
PATH = "screenshot.png" #A Filepath to an image on your computer"
title = "Uploaded with PyImgur"

im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title=title)
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.type)