from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('PgkdYLHFtKmMFcUvD8AMI50amBLbg7SD40QBdmmFqGfI4aYryIM0fbrtVwPUuEVGAU8Wls7dXIOn4G0WQi582zO9QoeKKC1LbXoKE6QA0YAcaANNJIwF+ooysnEdgwgIaLBFSttZG26A0D9cEXHEHQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e86bc3d7759e156eacb1b3e0dbb68fd6')


@app.route("/callback", methods=['POST'])
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()