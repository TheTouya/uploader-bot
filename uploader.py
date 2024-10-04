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
sponsor_channel = -100
# register admin user here in order to work properly
admin = 0
# Change this to True if you wanna require the sponsor channel
sponsor = False
@bot.message_handler(commands=["start"])
def greeting(msg):
    try:
       bot.reply_to(msg, "hello")
       if len(msg.text) > 1:
          user_stat[msg.from_user.id] = msg.text.split()[1]
          the_id = msg.text.split()[1]
          if sponsor:
            #if your channel is public, the link will appear, if not put the private link in "link" variable.
            channel = bot.get_chat(sponsor_channel)
            link = channel.username
            member = bot.get_chat_member(sponsor_channel, msg.from_user.id)
            if member.status in ["member", "creator", "administrator"]:
               bot.send_video(msg.from_user.id, file_id.get(the_id))
            else:
               markup = quick_markup({
                 "Check" :{"callback_data": "check"}
                }, row_width=1)
               bot.send_message(msg.from_user.id, f"join the sponsor channel {link}", reply_markup=markup)
          else:
             bot.send_video(msg.from_user.id, file_id.get(the_id))    
    except Exception as e:
       bot.reply_to(msg, "try again later")
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
   
@bot.callback_query_handler(func=lambda call:call.data == "check")
def checking_user(call):
   try:
      user = call.from_user.id
      member = bot.get_chat_member(sponsor_channel, user)
      if member.status in ["member", "creator", "administrator"]:
            file_id_1 = user_stat.get(user)
            bot.send_video(call.from_user.id, file_id.get(file_id_1))
            bot.delete_message(call.from_user.id, call.message.id)
      else:
         bot.answer_callback_query(call.id, "You didn't join yet", show_alert=True)
   except Exception as e:
      bot.send_message(call.from_user.id, "error ocurred. Try again later.")
      bot.send_message(admin, f"Error for {call.from_user.id} to get the video as {e}")

@bot.message_handler(commands=["pannel"])
def pannel(msg):
   try:
      if msg.from_user.id == admin:
         try:
            markup = quick_markup({
               "close ❌" : {"callback_data": "close"}
            }, row_width=1)
            sponsor_stat = ""
            files = len(file_id)
            the_admin = bot.get_chat(admin).first_name
            the_bot = bot.get_me().first_name
            if sponsor:
               sponsor_stat = "on"
            else:
               sponsor_stat = "off"
            phrase = f"<b>My name is {the_bot}\nMy admin is {the_admin}\nCurrently {files} videos are uploaded on me.\nThe sponsor is {sponsor_stat}</b>"
            bot.send_message(admin, phrase, parse_mode="HTML", reply_markup=markup)
         except Exception as e:
            bot.send_messageadmin, f"there was a problem with /pannel as {e}"
      else:
         bot.reply_to(msg, "You are not allowed")
   except Exception as e:
      bot.send_message(admin, f"{e}")


@bot.callback_query_handler(func=lambda call: call.data == "close")
def closing(call):
   try:
      if call.from_user.id == admin:
         bot.delete_message(call.from_user.id, call.message.id)
   except Exception as e :
      bot.send_message(admin, f"error in close callback data as {e}")

bot.infinity_polling()
