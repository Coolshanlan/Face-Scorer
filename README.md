# Personal Face Scorer line Bot
Face Scorer 是個臉部評分系統，由於每個人的審美觀不同，網路上現有的臉部評分器只能透過**通俗**的眼光給予評分，並不是按照**個人喜好**，因此 Face Scorer 透過 Line Bot 實現伊人一model 自己訓練屬於自己的臉部評分器，使用`我要看女/男生`，Line Bot 會自動上網抓10張男/女生照片，依照使用者給的分數建構資料集，在使用`請你看仔細`來訓練模型，完成屬於自己的臉部評分器，最後只要上傳想評分的照片即可。

## Screenshot
### 爬蟲建立資料集
<img src="https://github.com/Coolshanlan/Face-Scorer/blob/master/demo_image/Demo_image01.png?raw=true" width=40%><img src="https://github.com/Coolshanlan/Face-Scorer/blob/master/demo_image/Demo_image03.png?raw=true" width=40%>

### 訓練模型
<img src="https://github.com/Coolshanlan/Face-Scorer/blob/master/demo_image/Demo_image02.png?raw=true" width=24%>

### 照片評分
<img src="https://github.com/Coolshanlan/Face-Scorer/blob/master/demo_image/Demo_image04.png?raw=true" width=24%>

## Feature
- 我要看女生(Get 10 pictures of training date)
- 請你看仔細(Train model)
- upload image to get the Score
## Model
ResNet18
## Face recognition
You can see how to use Face recognition in [this repo](https://github.com/ageitgey/face_recognition)

## Line-Bot-sdk
You can find the document in [this repo](https://github.com/line/line-bot-sdk-python)

## How to use

### Setup Imgur access token
1. Login Imgur
2. go to setting > Applications
3. create new Application
4. get Client ID and Client secret
5. run imgurfile.getauthorize
6. check your pin code on the display URL
7. type pin code  to get access and refresh token
8. Write `Client ID`, `Client secret`, `access token`, `refresh token` on the top of `imgurfile.py`

### Setup Line Message API
- 登入自己帳號
- 創建Message API
- 進入 Messaging API 設定
  - Use webhook
  - 回應模式:聊天機器人
  - 加入好友歡迎訊息:停用
  - 自動回應訊息:停用

### Set line_secret_key
  - secret_key : Basic setting -> Channel secret
  - channel_access_token:Messaging API -> Channel access token

### ngrok
Use ngrok to setup a local server
1. download ngrok
2. cd to ngrok.exe Folder
3. 輸入cmd
  ```cmd
  ngrok http 5000 -region ap
  ```
4. copy https url and paste to Website of Messaging API -> webhook settings

## How to install

### Install dlib on windows
Don't use pip install dlib or conda

1. download whl file in https://pypi.org/simple/dlib/
2. pip install `whl file path`

### Install Face Recognition
You should install lib first

and type `pip install face_recognition` in cmd

### Requirements
```cmd
pip install -r requirements.txt
```
```
python=3.6
Pillow=5.3.0
cmake
dlib
face_recognition
imgurpython
pytorch
line-bot-sdk
flask
```
