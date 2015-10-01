ZAO
===

This is a long long story which started from a man
who engraved a "**早**" on his desktop. Since then,
there has been so many warriors who try to write
"**早**" to any place...

This is a telegram bot which allow you to say hello
to the world and know number of people who wake up ealier
than you.

In fact, this bot is pluggable, and easy to write plugins
to implement time-related jobs.

Requirements
------------

Python3 needed.(tested on python3.4)

Installation
------------

(on Archlinux)
```
$ git clone <this repo>
$ cd zaobot
$ virtualenv3 venv
$ . ./venv/bin/activate
(venv)$ pip install -r requirements.txt
```

Create a new bot and retrieve token from `BotFather` and
then save the token to token.txt

```
(venv)$ python start.py
```

TODO
----

* persistent storage with redis
* flush messages when booting
* list time of waking
