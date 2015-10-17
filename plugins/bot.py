"""
A simple plugin to anounce that "I am a bot"
"""
from . import TimerBot


class BotBot(TimerBot):
    def bind(self):
        @self.bot.message_handler(commands=['bot'])
        def hands_up(message):
            self.bot.reply_to(message, "<(=°ο°=)> 出现了，这是一只圈养的bot")
