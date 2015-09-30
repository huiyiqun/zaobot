import telebot
import logging
import threading
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from plugins.bot import BotBot
from plugins.bug import BugBot
from plugins.zao import ZaoBot

telebot.logger.setLevel(logging.DEBUG)

def readfile(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

sched = BackgroundScheduler()
bot = telebot.TeleBot(readfile('token.txt'))

BugBot(bot, sched).bind()
ZaoBot(bot, sched).bind()
BotBot(bot, sched).bind()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "大家好，我是周树人")

sched.start()
bot.polling()
