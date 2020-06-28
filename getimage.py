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
import urllib
import face_recognition
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw

# %%
url = 'https://www.shutterstock.com/zh-Hant/search/woman?kw=+%E5%A5%B3%E7%94%9F++%E7%B4%A0%E6%9D%90&gclid=Cj0KCQjw3Nv3BRC8ARIsAPh8hgIN0KN0j1woIrQtZb1ULfTSkzQAnyHGDnNj6eXi7D2WcG8vykOak0YaAnoqEALw_wcB&gclsrc=aw.ds&image_type=photo&mreleased=true&ethnicity=chinese&ethnicity=japanese&age=20s&gender=female&number_of_people=1&category=People&sort=newest&'
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "cookie": "did=zBOb8eYn9Tlem0/2yIXgJF0EUxfjMVFyPZeOg4s8GJw=; sstk.sid=s%3Ai6Yx5QK9IGQiuLkS3DH1A37bzp-rBMrs.xDwrptlsQvFlrdGrskyliw%2FPPzZCsycTxTfrIj0PLvY; visit_id=67077871683; visitor_id=61823879728; ajs_anonymous_id=%228edb3130-a273-48a8-9d7d-7e0566121c33%22; _ga=GA1.2.341957607.1593255045; _gid=GA1.2.1453567388.1593255045; _gcl_au=1.1.1319635990.1593255046; _CEFT=Q%3D%3D%3D; AMP_TOKEN=%24NOT_FOUND; IR_gbd=shutterstock.com; __ssid=dcd8f81b594ca3931801cf8a2b5f3c1; _actts=1593255048.1593255048.1593255048; _ym_uid=1593255048516771373; _ym_d=1593255048; _ym_isad=2; _actvc=1; locale=zh-Hant; IR_PI=0f37b1b7-b864-11ea-b127-42010a246104%7C1593343048255; _gcl_aw=GCL.1593256761.Cj0KCQjw3Nv3BRC8ARIsAPh8hgIN0KN0j1woIrQtZb1ULfTSkzQAnyHGDnNj6eXi7D2WcG8vykOak0YaAnoqEALw_wcB; _gcl_dc=GCL.1593256761.Cj0KCQjw3Nv3BRC8ARIsAPh8hgIN0KN0j1woIrQtZb1ULfTSkzQAnyHGDnNj6eXi7D2WcG8vykOak0YaAnoqEALw_wcB; IR_1305=1593256761340%7C76199%7C1593255047108%7C%7C; _actcc=28.18.28.18; footage_search_tracking_id=97c18393-dcea-4a81-932f-432eb88373b1; search=/search/woman?pl=PPC_GOO_TW_IG-346368958539&cr=bc&kw=%252B%25E5%25A5%25B3%25E7%2594%259F+%252B%25E7%25B4%25A0%25E6%259D%2590&gclid=Cj0KCQjw3Nv3BRC8ARIsAPh8hgIN0KN0j1woIrQtZb1ULfTSkzQAnyHGDnNj6eXi7D2WcG8vykOak0YaAnoqEALw_wcB&gclsrc=aw.ds&image_type=photo&mreleased=true&ethnicity=chinese&age=20s&gender=female&number_of_people=1&category=People; _gac_UA-32034-1=1.1593256798.Cj0KCQjw3Nv3BRC8ARIsAPh8hgIN0KN0j1woIrQtZb1ULfTSkzQAnyHGDnNj6eXi7D2WcG8vykOak0YaAnoqEALw_wcB; _actmu=79d596c1-0e98-4dfc-94cf-b12a77dbd55c; _actms=0b1fbb74-d11d-4be1-a438-068d8fafb120;_4c_=lVNbb9s2FP4rhQDlZZFNijcxgDHYTuYaLXJpU2TbiyGTtKXYFjWKsuoU%2Be87lO2syFOnB4Hn4%2FcdnuuPqCtMFV1hJknKuKSIM3YZbcyhia5%2BRKoO%2F334tW4bXUWF93VzNRx2XTdoitZ74xpv1Wag7G74UiQf88oPG5M7VQw7u8ur3%2Bvt6P5%2Bupjd3S0enxbzWUIoJzyTLGNEXig3WqqLTTeK00l8w%2BIxiyckvhGxpLH847ceFfGExmMU3%2FBYXscSXazVttSj6TP6NH147sjtnky%2BTLPxl3kzvi%2ByYj2%2FRZ9u0TPu7Nw9%2BL%2BX%2BNvn1ePXzcvDuDp8nF1Xt8%2Fc%2FFmK6%2FRJzbL9YXOXb9Bf%2Bbiy%2F9yMP3eLTk3CE41To7wb6Oai3OVrs%2FCH2ozqwnobXUamgqJEtdNwbhq%2FaUpvAOiZAWqXjXJl7UtbPYIOrtpKm1VZmaBoG%2BO%2B%2Bty3UORo3ZrGA6hsW3l3AMR3YOaVrQ472zZzDVBm9JJggpI8FSShWZ4lUgudCIMY5zjFipDehw5vYTnAeJAC4F%2FApBmCY%2B2sbpXv8wCwM8sPjd7AhTb7UplFV2pfBHHa009oYcp14QEWaY%2FWLlAGDM5dWWnbvded0Dcd4wLQpbMdJA32tHB2Zz5kIVwb8n%2FqBQ2YzqyMcz3r5zlbW7vemn7CQmmPlX4%2FfKcbGNx3lyHz0CscQt5alW%2BDHGYeBEaFBoE5Sadgz8aLb%2FNrMAnFkgmOxOC4FwxRFr1eRt%2BPi0IowTxFXEB9PWxFxikKHzBcqU8bEwmtMcZGJWqVy4RKBS1T0iSCoJzmVGQqXUZHnxxhRDCiglMGTvbl2Ych6cqklCQ4ZzqhOrRdCpRIkesVQ0u2UjJ6iyuFneJYZOe4cHYOq96ePOL%2FyLDs8CAnZzJ9S6Len9nsV3I%2B9jaBGiam%2Bl%2Fa19d%2FAQ%3D%3D",
    "referer": "https://www.google.com/",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}


# %%
# resp = requests.get(url+f"page={i}",headers=header)
# soup = BeautifulSoup(resp.text)
# print(resp.status_code)
# print(len(soup.find_all("div",{'class':"z_g_c"})))
# print(len(soup.find_all("img",{'class':"z_h_c z_h_e"})))
# for p in soup.find_all("img"):
#     print(p.get("src"))


# %%
# print(soup)


# %%


def getimage(num=1):
    imagepath = []
    while(1):
        page = random.randrange(1, 2062)
        resp = requests.get(url+f"page={page}", headers=header)
        soup = BeautifulSoup(resp.content)
        imagepathlist = [p['src']
                         for p in soup.find_all('img') if p.get("src") != None]
        imagepath = imagepathlist[random.randrange(0, len(imagepathlist))]
        with requests.get(imagepath, stream=True) as rq:
            rq.raise_for_status()  # check respose status
            with open("dataset/"+imagepath.split("/")[-1], "wb") as rw:
                for chunk in rq.iter_content(chunk_size=10000):
                    if chunk:
                        rw.write(chunk)
        image = face_recognition.load_image_file(
            "dataset/"+imagepath.split("/")[-1])
        face_locations = face_recognition.face_locations(image)
        print(face_locations)
        if len(face_locations) != 1:
            os.remove("dataset/"+imagepath.split("/")[-1])
            continue
        img = Image.fromarray(image)

        top, right, bottom, left = face_locations[0]
        top = int(top - top*0.6)
        left = int(left - left*0.14)
        right = int(right + right*0.14)
        bottom = int(bottom + bottom*0.11)
        image = image[top:bottom, left:right]
        img = Image.fromarray(image)
        img.save("dataset/"+imagepath.split("/")[-1])
        print(f"Save image {imagepath}")
        break
    return "dataset/"+imagepath.split("/")[-1], imagepath.split("/")[-1]
    # %%
    # for imp in imagepath:

    #     # methon 01
    #     # with  requests.get(img_url,stream=True) as rq :
    #     #     rq.raise_for_status()

    #         # img = Image.open(rq.raw)
    #         # img.save('{outdir}/{tag}.{ext}'.format(outdir=output_dir,tag=img_id,ext=img.format.lower()))
    #         # print(img.format.lower())

    #     # methon 02
    #     # urllib.request.urlretrieve(img_url,'{outdir}/{tag}.{ext}'.format(outdir=output_dir,tag=img_id,ext="jpg"))

    #     # methon 03
    #     with requests.get(imp, stream=True) as rq:
    #         rq.raise_for_status()  # check respose status
    #         with open("dataset/"+imp.split("/")[-1], "wb") as rw:
    #             for chunk in rq.iter_content(chunk_size=10000):
    #                 if chunk:
    #                     rw.write(chunk)

    #     print(f"Save image {imp}")
    # # 組合圖片而非網站的網址

    # # 對圖片送出請求


# # %%
# for i in range(0, 20):
#     getimage()
