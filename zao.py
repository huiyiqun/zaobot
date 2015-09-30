import telebot
import logging
import threading
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from plugins.bot import BotBot
from plugins.bug import BugBot

telebot.logger.setLevel(logging.DEBUG)

sched = BackgroundScheduler()

def readfile(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

def get_today():
    now = datetime.now()
    return (now.year, now.month, now.day)

today = get_today()
waken_guys = []
lock = threading.Lock()
stop = False
stop_until = None
bot = telebot.TeleBot(readfile('token.txt'))

BugBot(bot, sched).bind()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "大家好，我是周树人")

@bot.message_handler(commands=['zao'])
def zao(message):
    global today, waken_guys, lock
    with lock:
        if today != get_today():
            today = get_today()
            waken_guys = []
        if message.from_user.id in waken_guys:
            bot.reply_to(message, "Pia!<(=ｏ ‵-′)ノ☆ 你不是起床过了吗?")
        else:
            if len(waken_guys) == 0:
                bot.reply_to(message, "<(=ㄒ﹏ㄒ=)> 获得成就[最早起床]")
            else:
                bot.reply_to(message, "你是第{:d}起床的少年".format(len(waken_guys)+1))
            waken_guys.append(message.from_user.id)

BotBot(bot, sched).bind()

sched.start()
bot.polling()
