"""
A simple plugin to record waken people and return order of waking.
"""
import logging
from . import TimerBot
from datetime import datetime, timedelta, date
from threading import Lock
from redis_variable import RedisVariable

logger = logging.getLogger(__name__)

class ZaoBot(TimerBot):
    def __init__(self, *args, **kwargs):
        self.new_day()
        self.guys_mapping = RedisVariable('zaobot:guys_mapping')  # map id to Name
        self.lock = Lock()
        super().__init__(*args, **kwargs)

    def _list_guys(self):
        '''
        return list of guys as tuple(`name`, `time`) which is sorted by date
        '''
        result = self.waken_guys.zrange(0, -1, withscores=True)
        logger.debug('list_guys: result from redis is {}'.format(result))
        # Transform result from redis ( (timestamp(byte), id(byte)) )
        # to result we need ( (name(str), time(datetime)) )
        def trans_func(id_timestamp):
            uid, timestamp = id_timestamp
            name = self.guys_mapping.hget(int(uid)).decode(encoding='UTF-8')
            logger.debug('list_guys: id -> name {}:{}'.format(uid, name))
            logger.debug('type of name: {}'.format(type(name)))
            time = datetime.fromtimestamp(int(timestamp))
            return (name, time)

        ret = map(trans_func, result)
        # logger.debug('list_guys: result after map is {}'.format(list(ret)))
        return list(ret)

    def _who(self, user):
        return '少年'

    def new_day(self):
        self.waken_guys = RedisVariable('zaobot:waken_guys:{}'.format(
            str(date.today())))

    def bind(self):
        @self.sched.scheduled_job('cron', hour='5')
        def clear_guys():
            self.new_day()

        @self.bot.message_handler(commands=['zaoguys'])
        def list_guys(message):
            sorted_guys = self._list_guys()
            logger.debug('sorted_guys is {}'.format(list(sorted_guys)))
            if sorted_guys:
                self.bot.reply_to(
                    message,
                    '\n'.join(map(lambda i_guy: '{}. {}, {}'.format(i_guy[0]+1, *i_guy[1]), enumerate(sorted_guys))))
            else:
                self.bot.reply_to(message, 'o<<(≧口≦)>>o 还没人起床')

        @self.bot.message_handler(commands=['zao'])
        def bug(message):
            # save name to redis
            if message.from_user.last_name is None:
                name = message.from_user.first_name
            else:
                name = message.from_user.first_name + ' ' + message.from_user.last_name
            self.guys_mapping.hset(message.from_user.id, name)

            with self.lock:
                # There seems no way to determine whether an element in
                # sorted set except trying to retrieve it.
                rank = self.waken_guys.zrank(message.from_user.id)
                index = self.waken_guys.zcard()
                if rank is None:
                    self.waken_guys.zadd(message.date, message.from_user.id)
                    rewaken = False
                else:
                    rewaken = True

            # Send response
            if rewaken:
                self.bot.reply_to(message, "Pia!<(=ｏ ‵-′)ノ☆ 你不是起床过了吗?")
            else:
                if index == 0:
                    self.bot.reply_to(message, "<(=ㄒ﹏ㄒ=)> 获得成就[最早起床]")
                else:
                    self.bot.reply_to(message, "你是第{:d}起床的{}".format(index+1, self._who(message.from_user)))
