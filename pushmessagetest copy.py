from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import threading
cred = credentials.Certificate("Bear_sdk.json")
firebase_admin.initialize_app(cred)
db=firestore.client()


line_bot_api = LineBotApi('l9HWHyXh9dVumo0cqyRcRr+YfBZnB7ENKUh7qiIpHz36SylXwq9k3udoshU6pzqRQOEoSw0p1iW53urA2lVVRk1Z0QMeSQ+z0kPnIIM4zdAOQ7MbW2AFP3P1qVB8bkCFaFz7wHIXj8nLeV73sR2PnAdB04t89/1O/w1cDnyilFU=')

try:
    line_bot_api.push_message('Cf422bfecfa25f1295781b976cc1bdcfb', ImageSendMessage(original_content_url='https://cdn.discordapp.com/attachments/935386846127620097/948139457322811422/Red.png',preview_image_url='https://cdn.discordapp.com/attachments/935386846127620097/948139457322811422/Red.png'))
    line_bot_api.push_message('Cf422bfecfa25f1295781b976cc1bdcfb', TextSendMessage(text='คุณ พ่อเชม มีเกณฑ์การตรวจสอบอยู่ในระดับอันตรายสูง (แดง) \nกรุณาทำการตรวจอีกครั้งทันที หรือ ควรไปพบแแพทย์พร้อมเอกสารการตรวจสอบภายในแอป'))
    # line_bot_api.push_message('Ce5e442a18d3fef36ab47b3cd5af602fb', TextSendMessage(text='คุณ ปู่ดวงมี ศรีสุข เกณฑ์การตรวจสอบอยู่ในระดับอันตราย (ส้ม) \nให้ทำการตรวจอีกครั้งใน 5 นาที'))
    line_bot_api.push_message('Ude647d91b563e57ccf66573295ec2fee', ImageSendMessage(original_content_url='https://cdn.discordapp.com/attachments/935386846127620097/948139457322811422/Red.png',preview_image_url='https://cdn.discordapp.com/attachments/935386846127620097/948139457322811422/Red.png'))
    line_bot_api.push_message('Ude647d91b563e57ccf66573295ec2fee', TextSendMessage(text='คุณมีเกณฑ์การตรวจสอบอยู่ในระดับอันตรายสูง (แดง) \nกรุณาทำการตรวจอีกครั้งทันที หรือ ควรไปพบแแพทย์พร้อมเอกสารการตรวจสอบภายในแอป'))
   
except LineBotApiError as e:
    # error handle
    ...