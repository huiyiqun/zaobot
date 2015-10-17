"""
A plugin to record and remind of event
"""
import dateparser
from functools import wraps
from datetime import datetime, timedelta
from telebot import types as teletypes
from . import TimerBot


# FIXME: instance method only
def allow_type(type_list):
    def wrapper(f):
        @wraps(f)
        def wrapped(self, *args, **kwargs):
            message = kwargs.get('message', None) or args[0]
            if message.content_type not in type_list:
                self.bot.reply_to(message, 'Ooops, 类型不太对')
                return
            return f(self, *args, **kwargs)
        return wrapped
    return wrapper


class Event:
    pass


class EventBot(TimerBot):

    plan = [(timedelta(days=2), "身在水深火热的国度的小伙伴可以出发了。"),
            (timedelta(hours=1), "还在五道口堵车的少年可以开始跑步前进了。"),
            (timedelta(seconds=30), "坐等直播的少年可以开始开电脑了。"),
            (timedelta(seconds=3), "好了，开始happy吧。")]

    def __init__(self, *args, **kwargs):
        # Map chat_id to event
        self.current_events = {}
        # Map chat_id to map(title as key) of created events
        self.created_events = {}
        super().__init__(*args, **kwargs)

    def create_event(self, chat, event):
        if chat.id not in self.created_events:
            self.created_events[chat.id] = {}
        self.created_events[chat.id][event.title] = event
        # TODO: Schedule event
        for advance, note in self.plan:
            self.sched.add_job(self.remind_event, 'date', (chat, event, note),
                               run_date=event.time-advance)
        self.sched.add_job(self.delete_event, 'date', (chat, event),
                           run_date=event.time)

    def delete_event(self, chat, event):
        del self.created_events[chat.id][event.title]

    def remind_event(self, chat, event, note):
        self.bot.send_message(
            chat.id,
            '[{}]还有{}, {}'.format(
                event.title, event.time - datetime.now(), note))

    def list_event(self, chat):
        pass

    def bind(self):
        @self.bot.message_handler(commands=['addevent'])
        def add_event(message):
            msg = self.bot.reply_to(
                message, 'OK，有啥新活动？',
                reply_markup=teletypes.ForceReply(selective=True))
            self.current_events[message.chat.id] = Event()
            self.bot.register_for_reply(msg, self.step_event_title)

    @allow_type(['text'])
    def step_event_title(self, message):
        event = self.current_events[message.chat.id]
        event.title = message.text
        msg = self.bot.reply_to(
            message, '啥时候呢？',
            reply_markup=teletypes.ForceReply(selective=True))
        self.bot.register_for_reply(msg, self.step_event_time)

    @allow_type(['text'])
    def step_event_time(self, message):
        event = self.current_events[message.chat.id]
        event.time = dateparser.parse(message.text)
        if event.time is None:
            self.bot.reply_to(message, '听不懂...')
            return

        del self.current_events[message.chat.id]
        self.create_event(message.chat, event)
        self.bot.reply_to(message, '吼~')
