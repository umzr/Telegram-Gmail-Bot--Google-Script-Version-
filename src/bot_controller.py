#update on 2021-08-11
import datetime
import telebot
import time
from quickstart import main

#for Demo use. It is risky to plate your API KEY on the program.
#Better to use .ENV to store your API_KEY
API_KEY = '<HTTP API>'
bot = telebot.TeleBot(API_KEY)

mmbot_on_off = 0

@bot.message_handler(commands=['bot'])
def bot_(message):

  while True:
    time.sleep(30)

    req = main()
    if len(req) > 0:
        print(str(datetime.datetime.now() )+": ")
        print(len(req))

        for reqs in reversed(req):
            bot.send_message("<Your Chat ID>", "last sync: "+str(datetime.datetime.now() ) + "\n● " +reqs)
    else: print(str(datetime.datetime.now() )+ ": no message" )

@bot.message_handler(commands=['on'])
def on(message):
    global mbot_on_off
    mbot_on_off = 1
    bot.send_message(message.chat.id, "ON")

@bot.message_handler(commands=['off'])
def off(message):
    global mbot_on_off
    mbot_on_off = 0
    bot.send_message(message.chat.id, "off")


bot.polling()
