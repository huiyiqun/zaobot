import telebot
import logging

telebot.logger.setLevel(logging.DEBUG)

def readfile(filename):
    with open(filename, 'r') as f:
        return f.read()

bot = telebot.TeleBot(readfile('token.txt'))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "大家好，我是周树人")

bot.polling()
