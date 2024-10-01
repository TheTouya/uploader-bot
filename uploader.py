import os
import re
import telebot
from telebot.util import quick_markup
# comment the script below if you dont have an .env file
from dotenv import load_dotenv
# comment the script below if you dont have an .env file
load_dotenv()
API_KEY = os.getenv("API")
# register your bot here
bot = telebot.TeleBot(API_KEY, parse_mode=None)
# The videos' ids are saved here
file_id = {}
# use this in order to save the stats of a user
user_stat = {}
# if you have a sponsor channel save it here
sponsor_channel = -10012345678
# register admin user here in order to work properly
admin = 123345678
@bot.message_handler(commands=["start"])
def greeting(msg):
    try:
        if len(msg.text) > 1:
          user_stat[msg.from_user.id] = msg.text.split()[1]
          name = msg.text.split()[1]
          member = bot.get_chat_member(sponsor_channel, msg.from_usrer.id)
          if member in ["member", "creator", "administrator"]:
            bot.send_video(msg.from_user.id, file_id.get(name))
          else:
             markup = quick_markup({
                "Check" :{"callback_data": "check"}
             }, row_width=1)
             bot.send_message(msg.from_user.id, "You have to join our sponsor channel", reply_markup=markup)
        else:
          bot.reply_to(msg, "What can I do for you?")
    except Exception as e:
       bot.reply_to(msg, "sorry there has been an error")
       bot.send_message(admin, f"error as {e}")

@bot.message_handler(content_types=["video"])
def getting_id(msg):
   try:
      if msg.from_user.id == admin:
         if msg.content_type == "video":
            vid_id = msg.video.file_id
            vid_name = ""
            for x in range(0,7):
              vid_name += vid_id[::-1][x]
            file_id[vid_name] = vid_id
            bot.send_message(msg.from_user.id, f"https://t.me/thetouyastesterbot?start={vid_name}")
         else:
            bot.reply_to(msg, "This type of content is not supported")
   except Exception as e:
      bot.send_message(admin, f"Error in creating your video link as {e}")
   
@bot.callback_query_handler(func=lambda call:call.id == "check")
def checking_user(call):
   try:
      user = call.from_user.id
      member = bot.get_chat_member(user, sponsor_channel)
      if member in ["member", "creator", "administrator"]:
            file_id_1 = user_stat.get(user)
            bot.send_video(call.from_user.id, file_id.get(file_id_1))
      else:
         bot.answer_callback_query("You didn't join yet", show_alert=True)
   except Exception as e:
      bot.send_message(call.from_user.id, "error ocurred. Try again later.")
      bot.send_message(admin, f"Error for {call.from_user.id} to get the video as {e}")

bot.infinity_polling()
