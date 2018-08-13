#!/usr/bin/env python3

from functools import wraps
from hatsunebot import config

from telegram.ext.dispatcher import run_async
from telegram import ReplyKeyboardMarkup


def sep(num, none_is_zero=False):
    if num is None:
        return 0 if none_is_zero is True else None
    return "{:,}".format(num)


@run_async
def common_help(bot, update):

    custom_keyboard = [["Random"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    cid = update.message.chat.id
    bot.send_message(chat_id=cid, text="Please use this",
                     reply_markup=reply_markup)


def full_list(in_list):

    if len(in_list) < config.FIVE_TYPE_LIST_MAX_LENGTH:
        if len(in_list) > config.FIVE_TYPE_LIST_MIN_LENGTH:
            in_list.append("None")
            full_list(in_list)
        else:
            raise Exception
    else:
        return in_list


@run_async
def invalid_command(bot, update):
    # text = "This command is invalid"
    text = "Hi~"
    update.message.reply_text(text=text, quote=True)
    pass


def only_admin(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.message.from_user.id not in config.ADMINS:
            invalid_command(bot, update, *args, **kwargs)
            return
        else:
            common_help(bot, update, *args, **kwargs)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped
