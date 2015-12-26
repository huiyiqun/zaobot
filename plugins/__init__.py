class TimerBot:
    def __init__(self, bot, sched):
        self.bot = bot
        self.sched = sched

    @staticmethod
    def retrieve_args(message):
        cmd = message.text.split(maxsplit=1)
        if len(cmd) == 1:
            return None
        else:
            return cmd[-1]
