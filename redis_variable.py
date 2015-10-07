from redis import StrictRedis as Redis

# Default redis client
r = Redis()

OBJECT_ORIENTED_OPERATIONS = [
    'append',
    'blpop',
    'brpop',
    'debug_object',
    'decr',
    'delete',  # SET_ORIENTED_OPERATION
    'exists',
    'expire',
    'expireat',
    'get',
    'getbit',
    'getset',
    'hdel',
    'hexists',
    'hget',
    'hgetall',
    'hincrby',
    'hkeys',
    'hlen',
    'hmget',
    'hmset',
    'hset',
    'hsetnx',
    'hvals',
    'incr',
    'lindex',
    'linsert',
    'llen',
    'lpop',
    'lpush',
    'lpushx',
    'lrange',
    'lrem',
    'lset',
    'ltrim',
    'move',
    'persist',
    'rpush',
    'rpushx',
    'sadd',
    'scard',
    'sdiffstore',
    'set',
    'setbit',
    'setex',
    'setnx',
    'setrange',
    'sinterstore',
    'sismember',
    'smember',
    'sort',
    'spop',
    'sramdmember',
    'srem',
    'strlen',
    'substr',
    'sunionstore',
    'ttl',
    'type',
    'unwatch',  # Need to confirm
    'watch',  # SET_ORIENTED_OPERATION
    'zadd',
    'zcard',
    'zincrby',
    'zinterstore',
    'zrange',
    'zrangebyscore',
    'zrank',
    'zrem',
    'zrem',
    'zremrangebyrank',
    'zremrangebyscore',
    'zrevrange',
    'zrevrangebyscore',
    'zrevrank',
    'zscore',
    'zunionstore',
]

RELATION_ORIENTED_OPERATIONS = [
    'brpoplpush',
    'rename',
    'renamenx',
    'rpoplpush',
    'smove',
]

DB_ORIENTED_OPERATIONS = [
    'bgrewriteof',
    'bgsave',
    'config_get',
    'config_set',
    'echo',
    'execute_command',
    'flushall',
    'flushdb',
    'info',
    'keys',
    'lastsave',
    'mget',
    'mset',
    'msetnx',
    'object',
    'parse_response',
    'ping',
    'pipeline',
    'publish',
    'pubsub',
    'randomkey',
    'save',
    'set_response_callback',
    'shutdown',
    'slaveof',
    'slowlog_get',
    'slowlog_len',
    'slowlog_reset',
    'transaction',
    'lock',
]

OPERATIONS_NOT_SUPPORTED = [
    'sdiff',  # LIST_ORIENTED_OPERATION
    'sinter',  # LIST_ORIENTED_OPERATION
    'sunion',  # LIST_ORIENTED_OPERATION
]


class NoSuchOperation(Exception):
    pass


class NotSupported(Exception):
    pass


def relation_oriented_operation_factory(func):
    def g(*args, **kwargs):
        if len(args) > 1:
            src, dst, *args = args
        else:
            src, *args = args
            dst = kwargs.pop('dst')

        if isinstance(dst, RedisVariable):
            dst = dst.key

        return func(src, dst, *args, **kwargs)
    return g


class RedisVariable:
    def __init__(self, key, redis=None):
        self.key = key
        if redis is None:
            global r
            self.redis = r
        else:
            self.redis = redis

    def __getattr__(self, name):
        global OBJECT_ORIENTED_OPERATIONS
        global RELATION_ORIENTED_OPERATIONS
        global DB_ORIENTED_OPERATIONS
        global OPERATIONS_NOT_SUPPORTED
        func = getattr(self.redis, name, None)
        if func is None:
            raise NoSuchOperation()
        elif name in OBJECT_ORIENTED_OPERATIONS:
            return lambda *args, **kwargs: func(self.key, *args, **kwargs)
        elif name in RELATION_ORIENTED_OPERATIONS:
            func = relation_oriented_operation_factory(func)
            return lambda *args, **kwargs: func(self.key, *args, **kwargs)
        elif name in DB_ORIENTED_OPERATIONS:
            return lambda *args, **kwargs: func(*args, **kwargs)
        elif name in OPERATIONS_NOT_SUPPORTED:
            raise NotSupported()
        else:
            raise NotSupported('New operation?')
