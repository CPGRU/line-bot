import swisstime
swisstime.start()

from flask import Flask, request, abort
from dotenv import load_dotenv
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

load_dotenv()

name = "Swiss_Life"
lineapp = Flask(name)

line_token = os.getenv("LINE_TOKEN")
line_channel_secret = os.getenv("LINE_CHANNEL_SECRET")
line_bot_api = LineBotApi(line_token)
handler = WebhookHandler(line_channel_secret)


@lineapp.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    lineapp.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = "想查詢瑞士資訊嗎? 請輸入:天氣, 時間, 旅遊 及 相關文章"
    if msg in ['hi', 'Hi', '你好'] :
        r = '你好'
    elif msg == '你是誰':
        r = '我是機器人'
    

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if name == "main":
    lineapp.run()