"""
A simple plugin to let bot down for several minutes
This bot should bind ealier than any others.
"""
from . import TimerBot
from datetime import datetime, timedelta

class BugBot(TimerBot):
    def __init__(self, *args, **kwargs):
        self.sleeping = False
        self.sleeping_place = None
        super().__init__(*args, **kwargs)

    def bind(self):
        @self.bot.message_handler(func=lambda _: self.sleeping)
        def sleep(message):
            pass

        @self.bot.message_handler(commands=['bug'])
        def bug(message):
            # FIXME: Race-condition
            self.sleeping = True
            self.sleeping_place = message
            self.sched.add_job(self.wake, 'date', run_date=datetime.now()+timedelta(seconds=30))
            self.bot.reply_to(message, "烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫...")

    def wake(self):
        self.sleeping = False
        self.bot.send_message(self.sleeping_place.chat.id, "<(=ㄒ﹏ㄒ=)> 终于从臭水沟里爬出来了")
