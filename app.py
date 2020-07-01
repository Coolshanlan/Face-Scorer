# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os
import re
import requests
import torch
import getimage
import numpy as np
import FaceScoreAnilysis as FSA
import FaceDetect as FD
import face_recognition
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from urllib.parse import parse_qs
import imgurfile
from imgurpython import ImgurClient
from linebot.models.template import *
from linebot.models.template import (
    ButtonsTemplate, CarouselTemplate, ConfirmTemplate, ImageCarouselTemplate
)
from linebot.models import (
    PostbackEvent
)
from linebot.models import (
    FollowEvent
)
from linebot.models import (
    ImagemapSendMessage, TextSendMessage, ImageSendMessage, LocationSendMessage, FlexSendMessage, VideoSendMessage
)
import json
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage
)
from flask import Flask, request, abort
from IPython import get_ipython

# %%
# get_ipython().system('pip install flask')
# get_ipython().system('pip install line-bot-sdk')


# %%
'''

整體功能描述

應用伺服器主結構樣板
    用來定義使用者傳送消息時，應該傳到哪些方法上
        比如收到文字消息時，轉送到文字專屬處理方法

消息專屬方法定義
    當收到文字消息，從資料夾內提取消息，並進行回傳。

啟動應用伺服器

'''


# %%
'''

Application 主架構

'''

# 引用Web Server套件

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別

# 引用無效簽章錯誤

# 載入json處理套件

# 載入基礎設定檔
secretFileContentJson = json.load(
    open("./line_secret_key", 'r', encoding='utf8'))

# 設定Server啟用細節
app = Flask(__name__, static_url_path="/material", static_folder="./material/")

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))

# 啟動server對外接口，使Line能丟消息進來


@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# %%
'''

消息判斷器

讀取指定的json檔案後，把json解析成不同格式的SendMessage

讀取檔案，
把內容轉換成json
將json轉換成消息
放回array中，並把array傳出。

'''

# 引用會用到的套件


def detect_json_array_to_new_message_array(fileName):

    # 開啟檔案，轉成json
    with open(fileName, 'r', encoding='utf8') as f:
        jsonArray = json.load(f)

    # 解析json
    returnArray = []
    for jsonObject in jsonArray:

        # 讀取其用來判斷的元件
        message_type = jsonObject.get('type')

        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(
                ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(
                TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(
                StickerSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'location':
            returnArray.append(
                LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'video':
            returnArray.append(VideoSendMessage.new_from_json_dict(jsonObject))

    # 回傳
    return returnArray


# %%
'''

handler處理關注消息

用戶關注時，讀取 素材 -> 關注 -> reply.json

將其轉換成可寄發的消息，傳回給Line

'''

# 引用套件

# 關注事件處理


@handler.add(FollowEvent)
def process_follow_event(event):

    # 讀取並轉換
    result_message_array = []
    replyJsonPath = "material/follow/reply.json"
    result_message_array = detect_json_array_to_new_message_array(
        replyJsonPath)

    # 消息發送
    line_bot_api.reply_message(
        event.reply_token,
        result_message_array
    )

    # # 從follow資料夾內，取出圖文選單id，並告知line，綁定用戶
    # linkRichMenuId = open("material/follow/rich_menu_id", 'r').read()
    # line_bot_api.link_rich_menu_to_user(event.source.user_id, linkRichMenuId)


# %%
'''

handler處理文字消息

收到用戶回應的文字消息，
按文字消息內容，往素材資料夾中，找尋以該內容命名的資料夾，讀取裡面的reply.json

轉譯json後，將消息回傳給用戶

'''

# 引用套件


@handler.add(MessageEvent, message=ImageMessage)
def process_image_message(event):
    result_message_array = []
    # response = requests.get(
    #     f"https://api.line.me/v2/bot/message/{event.message.id}/content", stream=True, headers={'Authorization': f'Bearer {secretFileContentJson.get("channel_access_token")}'})

    # img = Image.open(response.raw)
    # filepath = f"predection/{event.message.id}.{img.format.lower()}"
    # img.save(filepath)
    filepath = "predection/308992.jpg"
    img, rects = FD.getFaceRect(filepath)
    copyrect = [i for i in rects]
    Img = Image.fromarray(img)
    imgdrw = ImageDraw.Draw(Img)
    for i in range(0, len(rects)):
        top, right, bottom, left = rects[i]
        imgdrw.rectangle([(left, top), (right, bottom)],
                         outline=(255, 0, 0), width=10)
    rectResize = FD.resizeRect(rects)
    score = []
    scorestring = ""
    font = ImageFont.truetype('arial.ttf', 60)
    for i in range(len(rectResize)):
        top, right, bottom, left = rectResize[i]
        resizeimage = img[top:bottom, left:right]
        nowscore = round(FSA.prediction(resizeimage), 3)
        scorestring += str(nowscore)+"\n"
        top, right, bottom, left = copyrect[i]
        imgdrw.text((left, top-70), str(nowscore), (255, 0, 0), font=font)
        score.append(nowscore)
    Img.save(filepath)
    result_message_array.append(uploadImage(filepath.split('/')[-1], filepath))
    result_message_array.append(TextSendMessage(text=scorestring))
    line_bot_api.reply_message(
        event.reply_token,
        result_message_array
    )

# 文字消息處理


imagepath = ""
imagefilename = ""
remainphoto = 0


def uploadImage(filename, path):
    config = {
        'name': filename.split('.')[0],
        'title': path.split('.')[0],
        'description': 'test-description'
    }

    imageinfo = imgurfile.upload(imgur_client, path, config)
    imageurl = imageinfo['link']
    # with open("showimage.json", 'r', encoding='utf8') as f:
    #     showimagejson = json.load(f)
    result_message_array = ImageSendMessage(
        original_content_url=imageurl, preview_image_url=imageurl)
    return result_message_array


def GiveNewImage():
    global imagefilename, imagepath
    imagepath, imagefilename = getimage.getimage()
    result_message_array = uploadImage(imagefilename, imagepath)
    return result_message_array


@ handler.add(MessageEvent, message=TextMessage)
def process_text_message(event):
    global remainphoto, imagefilename, imagepath
    # 讀取本地檔案，並轉譯成消息
    result_message_array = []
    if remainphoto >= 0 and (re.fullmatch(r"(\d)", event.message.text.replace(" ", ""), re.X) != None or re.fullmatch(r"10", event.message.text.replace(" ", ""), re.X) != None):
        score = int(event.message.text.replace(" ", ""))
        if score > 10:
            score = 10
        elif score < 0:
            score = 0
        with open("train.csv", 'a', encoding='utf8') as f:
            f.write(imagefilename+","+str(score)+"\n")
        remainphoto -= 1
        if remainphoto >= 0:
            result_message_array.append(
                TextSendMessage(text=str(10-remainphoto)+"/10"))
            result_message_array.append(GiveNewImage())
    elif event.message.text == "我要看女生":
        replyJsonPath = "material/"+event.message.text+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(
            replyJsonPath)
        remainphoto = 9
        result_message_array.append(TextSendMessage(text="1/10"))
        result_message_array.append(GiveNewImage())
    elif event.message.text == "請你看仔細":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="模型訓練中...")
        )
        FSA.updateData()
        log = ""
        for i in range(5):
            acc, loss = FSA.train()
            acc = round(acc, 4)
            loss = round(loss, 4)
            log += f"loss:{loss}  acc:{acc}\n"
        log += "訓練完成！"
        line_bot_api.push_message(
            event.source.user_id,
            TextSendMessage(text=log)
        )
        return

    else:
        replyJsonPath = "material/"+"安安你好"+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(
            replyJsonPath)

    # 發送
    line_bot_api.reply_message(
        event.reply_token,
        result_message_array
    )


# %%
'''

handler處理Postback Event

載入功能選單與啟動特殊功能

解析postback的data，並按照data欄位判斷處理

現有三個欄位
menu, folder, tag

若folder欄位有值，則
    讀取其reply.json，轉譯成消息，並發送

若menu欄位有值，則
    讀取其rich_menu_id，並取得用戶id，將用戶與選單綁定
    讀取其reply.json，轉譯成消息，並發送

'''


@ handler.add(PostbackEvent)
def process_postback_event(event):

    query_string_dict = parse_qs(event.postback.data)
    print(event.postback.data)
    print(query_string_dict)
    if 'folder' in query_string_dict:

        result_message_array = []

        replyJsonPath = 'material/' + \
            query_string_dict.get('folder')[0]+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(
            replyJsonPath)

        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )
    elif 'menu' in query_string_dict:

        linkRichMenuId = open(
            "material/"+query_string_dict.get('menu')[0]+'/rich_menu_id', 'r').read()
        line_bot_api.link_rich_menu_to_user(
            event.source.user_id, linkRichMenuId)

        replyJsonPath = 'material/' + \
            query_string_dict.get('menu')[0]+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(
            replyJsonPath)

        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )


# %%
'''

Application 運行（開發版）

'''
# if __name__ == "__main__":
#     imgur_client = imgurfile.setauthorize()
#     # for i in range(15):
#     #     acc, loss = FSA.train()
#     #     acc = round(acc, 4)
#     #     loss = round(loss, 4)
#     #     print(f"loss:{loss}  acc:{acc}")
#     # process_image_message(None)
#     app.run(host='0.0.0.0')


# %%
'''

Application 運行（heroku版）

'''

if __name__ == "__main__":
    imgur_client = imgurfile.setauthorize()
    app.run(host='0.0.0.0', port=os.environ['PORT'])


# %%
