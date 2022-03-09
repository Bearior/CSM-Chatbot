from email import message
import profile
import base64
import os
import errno
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask,abort, request
import tempfile
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
from sqlalchemy import true

cred = credentials.Certificate("fame_sdk.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

app = Flask(__name__)

load_dotenv()

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
   
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

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
    profile = line_bot_api.get_profile(event.source.user_id)
    UserID = profile.user_id
    groupinfo = line_bot_api.get_group_summary(event.source.group_id)
    # group_member_ids = line_bot_api.get_group_member_ids(event.source.group_id)
    group_count = line_bot_api.get_group_members_count(event.source.group_id)
    Username = profile.display_name
    

    # if text == 'groupid':
    #         line_bot_api.reply_message(
    #             event.reply_token, [
    #                 TextSendMessage(text='Group ID : ' + groupinfo.group_id),
    
                    
    #             ]   
    #         )

    # if text == 'groupinfo':
    #         line_bot_api.reply_message(
    #             event.reply_token, [
    #                 TextSendMessage(text='Group name : ' + groupinfo.group_name),
    #                 ImageSendMessage(original_content_url=groupinfo.picture_url,
    #                                 preview_image_url=groupinfo.picture_url)
    #             ]   
    #         )
     
    # if text == 'members':
    #     line_bot_api.reply_message(
    #         event.reply_token,[
    #             TextSendMessage(text='We have '+ str(group_count + 1) + ' People in this group \n(including me!)'),
    #         ])

    if text == 'db':
        line_bot_api.reply_message(
            event.reply_token, [ 
                TextSendMessage(text='success')
            ])
        
        db.collection("N").document(UserID).set({
            "name" : profile.display_name,
            "status message" : profile.status_message,
            "certified" : "these are from firestore db"
    })
   
    doc_ref = db.collection(u'N').document(UserID)
    doc = doc_ref.get()
    get_name = doc_ref.get({u'name'})   
    name = u'{}'.format(get_name.to_dict()['name'])

    if text == 'read my data' :
        if doc.exists:
            line_bot_api.reply_message(
                event.reply_token, [ 
                    TextSendMessage((f'Document data: {doc.to_dict()}'))
                ])
        else:
            line_bot_api.reply_message(
                event.reply_token, [ 
                    TextSendMessage(u'document not found \n please send data by typing db ')
                ])
    
    if text == 'dbtest1' :
        if doc.exists:
            line_bot_api.reply_message(
                event.reply_token, [ 
                    TextSendMessage((f'name: {name}'))
                ])
        else:
            line_bot_api.reply_message(
                event.reply_token, [ 
                    TextSendMessage(u'document not found \n please send data by typing db ')
                ])

    if text == 'ติดตั้งระบบ':
        line_bot_api.reply_message(
            event.reply_token, [ 
                TextSendMessage(f'ติดตั้งระบบสำหรับ {Username} เรียบร้อย')
            ])
        
        db.collection('Groups').document(groupinfo.group_id).collection('Users').document(UserID).set({
            "name" : profile.display_name,
            "status message" : profile.status_message,
            "certified" : "these are from firestore db",
            "groupID" : groupinfo.group_id
    })

    # if text == 'sendgroup':
    #     doc_ref = db.collection(u'Groups').document()
    #     doc = doc_ref.where(u'LineUserID', u'==', UserID).get({u'groupID'})
    #     get_groupID = doc
    #     GroupID = u'{}'.format(get_groupID.to_dict()['groupID'])


    #     line_bot_api.push_message(GroupID, TextSendMessage(text='Send from Private'))

@handler.add(MessageEvent, message=(ImageMessage))
def handle_content_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    profile = line_bot_api.get_profile(event.source.user_id)
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
        tempfile_path = tf.name

        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)


        with open(dist_path, "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
        print(my_string)

        line_bot_api.reply_message(
            event.reply_token, [ 
                TextSendMessage(u'done!'),
            ])

        db.collection('Linepicture').document().set({
            'picturebase64' : str(my_string.decode('utf-8')),
            'UserID' : profile.user_id
        })
      
    else:
        return
    

if __name__ == "__main__":
    app.run()











