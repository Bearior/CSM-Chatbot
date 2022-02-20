from flask import Flask,abort, request
from linebot import (
    LineBotApi, WebhookHandler
)
from dotenv import load_dotenv
import os
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, PostbackEvent, StickerMessage, StickerSendMessage, 
    LocationMessage, LocationSendMessage, ImageMessage, ImageSendMessage, AudioMessage, AudioSendMessage)

app = Flask(__name__)

load_dotenv()

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

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
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    if text == 'members':
        if isinstance(event.source, SourceUser):
            group_id = line_bot_api.get_group_member_ids
            group_count = line_bot_api.get_group_members_count(group_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='number of people in this group :' + group_count),
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Please use this command in group chat"))
    if text == 'voice':
            AudioSendMessage(
            original_content_url='file:///D:/Mhee/GC+/NSC/CSM-Chatbot/voice_test.mp3', 
            duration=240000)
    else: TextSendMessage(text='error')


if __name__ == "__main__":
    app.run()