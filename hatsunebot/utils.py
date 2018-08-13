#!/usr/bin/env python3

from functools import wraps
from hatsunebot import config

from telegram.ext.dispatcher import run_async


def sep(num, none_is_zero=False):
    if num is None:
        return 0 if none_is_zero is True else None
    return "{:,}".format(num)

def full_list(in_list):
    
    if in_list < 5:
        in_list.append("None")
        full_list(in_list)
    else:
        return in_list

@run_async
def invalid_command(bot, update):
    # text = "This command is invalid"
    text = "Hi!"
    update.message.reply_text(text=text, quote=True)
    pass


def only_admin(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.message.from_user.id not in config.ADMINS:
            invalid_command(bot, update, *args, **kwargs)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped
