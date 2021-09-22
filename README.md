# Personal Face Scorer line Bot
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
