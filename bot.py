import telegram
import cv2
import requests
from PIL import Image
from io import BytesIO
import json
import os
import numpy as np
from dotenv import load_dotenv
load_dotenv(".env")
from telegram.ext import(MessageHandler,
Updater,CommandHandler,Filters,ConversationHandler,CallbackContext,Filters
)
token=os.getenv("TOKEN")


def start(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id,text="Welcome to Mediciner")

def photo(update,context):
    print("here")
    user=update.message.from_user
    photo_file=update.message.photo[-1].get_file()
    response=requests.get(photo_file.file_path)
    r=requests.post(url="http://localhost:5000/process",files={"file":BytesIO(response.content)})
    data=json.loads(r.text)
    context.bot.send_message(chat_id=update.effective_chat.id,text=f"Name of medicine : {data['text']}")




if __name__=="__main__":
    print("starting")
    updater=Updater(token,use_context=True)
    dispather=updater.dispatcher
    start_handler=CommandHandler("start",start)
    dispather.add_handler(start_handler)
    photo_handler=MessageHandler(Filters.photo,photo)
    dispather.add_handler(photo_handler)
    updater.start_polling(poll_interval=0.5,read_latency=0.5)
