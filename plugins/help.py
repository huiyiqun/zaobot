"""
A simple plugin to print help
"""
from . import TimerBot


class HelpBot(TimerBot):
    def bind(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def hello(message):
            self.bot.reply_to(message, "大家好，我是周树人。")
