"""
A simple plugin to record waken people and return order of waking.
"""
from . import TimerBot
from datetime import datetime, timedelta
from threading import Lock

class ZaoBot(TimerBot):
    def __init__(self, *args, **kwargs):
        self.waken_guys = []
        self.lock = Lock()
        super().__init__(*args, **kwargs)

    def bind(self):
        @self.sched.scheduled_job('cron', hour='3')
        def clear_guys():
            self.waken_guys = []
        
        @self.bot.message_handler(commands=['zao'])
        def bug(message):
            with self.lock:
                if message.from_user.id not in self.waken_guys:
                    self.waken_guys.append(message.from_user.id)
                    rewaken = False
                else:
                    rewaken = True

            # Send response
            index = self.waken_guys.index(message.from_user.id)
            if rewaken:
                self.bot.reply_to(message, "Pia!<(=ｏ ‵-′)ノ☆ 你不是起床过了吗?")
            else:
                if index == 0:
                    self.bot.reply_to(message, "<(=ㄒ﹏ㄒ=)> 获得成就[最早起床]")
                else:
                    self.bot.reply_to(message, "你是第{:d}起床的少年".format(index))