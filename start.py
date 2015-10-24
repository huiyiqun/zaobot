import telebot
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from plugins.bot import BotBot
from plugins.bug import BugBot
from plugins.zao import ZaoBot
from plugins.help import HelpBot
from plugins.event import EventBot

telebot.logger.setLevel(logging.DEBUG)


def readfile(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

sched = BackgroundScheduler()
bot = telebot.TeleBot(readfile('token.txt'))

#BugBot(bot, sched).bind()
ZaoBot(bot, sched).bind()
BotBot(bot, sched).bind()
HelpBot(bot, sched).bind()
EventBot(bot, sched).bind()

sched.start()
bot.polling(none_stop=True)
