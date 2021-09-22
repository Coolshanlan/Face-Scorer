# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# https://www.shutterstock.com/zh-Hant/search/woman?pl=PPC_GOO_TW_IG-346368958539&cr=bc&kw=%2B%E5%A5%B3%E7%94%9F+%2B%E7%B4%A0%E6%9D%90&gclid=Cj0KCQjw3Nv3BRC8ARIsAPh8hgIN0KN0j1woIrQtZb1ULfTSkzQAnyHGDnNj6eXi7D2WcG8vykOak0YaAnoqEALw_wcB&gclsrc=aw.ds&image_type=photo&mreleased=true&ethnicity=chinese&age=20s&gender=female&number_of_people=1&category=People


# %%
import random
import requests
import os
from bs4 import BeautifulSoup
from PIL import Image
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import FaceDetect
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
import urllib
# %%
urlman = "https://www.shutterstock.com/zh-Hant/search/%E7%94%B7?gclid=Cj0KCQjw3Nv3BRC8ARIsAPh8hgIN0KN0j1woIrQtZb1ULfTSkzQAnyHGDnNj6eXi7D2WcG8vykOak0YaAnoqEALw_wcB&gclsrc=aw.ds&image_type=photo&mreleased=true&ethnicity=chinese&age=20s&gender=male&category=People&editorial=0&number_of_people=1"
urlwoman = 'https://www.shutterstock.com/zh-Hant/search/%E6%BC%82%E4%BA%AE?kw=%E5%A5%B3%E7%94%9F+%2B%E7%B4%A0%E6%9D%90&gclid=Cj0KCQjw3Nv3BRC8ARIsAPh8hgIN0KN0j1woIrQtZb1ULfTSkzQAnyHGDnNj6eXi7D2WcG8vykOak0YaAnoqEALw_wcB&gclsrc=aw.ds&image_type=photo&mreleased=true&gender=female&category=People&number_of_people=1&safe=off&age=20s&ethnicity=japanese&sort=newest'
header= {
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
driver_path=r'C:\UserD\Program\Project_Python\LineBot\chromedriver.exe'
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
opt = webdriver.ChromeOptions()
opt.add_argument('--user-agent=%s' % user_agent)
driver = webdriver.Chrome(driver_path,chrome_options=opt)
speed=False
def getimage(num=1, sex=0):
    imagepath = []
    local_url = ""
    while(1):
        if sex == 0:
            local_url = urlman
            page = random.randrange(1, 438)
        else:
            local_url = urlwoman
            page = random.randrange(1, 1988)
        if speed:
            resp = requests.get(local_url+f"page={page}", headers=header)
            soup = BeautifulSoup(resp.content)
        else:
            driver.get(local_url+f"&page={page}")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            source = driver.page_source
            soup = BeautifulSoup(source)
        print(page)
        imagepathlist = [p['src'] for p in soup.find_all('img') if p.get("src")!=None]
        imagepath = imagepathlist[random.randrange(0, len(imagepathlist))]
        with requests.get(imagepath, stream=True) as rq:
            rq.raise_for_status()  # check respose status
            with open("dataset/"+imagepath.split("/")[-1], "wb") as rw:
                for chunk in rq.iter_content(chunk_size=10000):
                    if chunk:
                        rw.write(chunk)
        # image = face_recognition.load_image_file(
        #     "dataset/"+imagepath.split("/")[-1])
        image, face_locations = FaceDetect.getFaceRect(
            "dataset/"+imagepath.split("/")[-1])
        if len(face_locations) != 1:
            os.remove("dataset/"+imagepath.split("/")[-1])
            continue
        face_locations = FaceDetect.resizeRect(face_locations)
        img = Image.fromarray(image)
        top, right, bottom, left = face_locations[0]
        image = image[top:bottom, left:right]
        img = Image.fromarray(image)
        img.save("dataset/"+imagepath.split("/")[-1])
        print(f"Save image {imagepath}")
        break
    return "dataset/"+imagepath.split("/")[-1], imagepath.split("/")[-1]
