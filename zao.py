import telebot
import logging
import threading
from datetime import datetime, timedelta

telebot.logger.setLevel(logging.DEBUG)

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

@bot.message_handler(func=lambda message: stop)
def sleep(message):
    global stop_until, stop
    if stop_until > datetime.now():
        stop = False
        bot.send_message(message.chat.id, "<(=ㄒ﹏ㄒ=)> 终于从臭水沟里爬出来了")

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

@bot.message_handler(commands=['bug'])
def bug(message):
    global stop, stop_until
    stop = True
    stop_until = datetime.now() + timedelta(minutes=5)
    bot.reply_to(message, "烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫...")

@bot.message_handler(commands=['bot'])
def hands_up(message):
    bot.reply_to(message, "<(=°ο°=)> 出现了，这是一只圈养的bot")

bot.polling()
