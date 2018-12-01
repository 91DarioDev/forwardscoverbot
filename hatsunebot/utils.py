#!/usr/bin/env python3

from functools import wraps
from hatsunebot import config

from telegram.ext.dispatcher import run_async
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import ParseMode


@run_async
def AdminKeyboard(bot, update):
    '''
    show the help icon for admin

    "/CheckExistedOrNot\n\n"
    "/CheckResultShow\n\n"

    delete the "/CheckAllData"
    '''
    custom_keyboard = [["/Show"], ["/ForwardStateTransition"],
                       ["/CheckExistedOrNot", "/CheckResultShow"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    cid = update.message.chat.id
    text = "What's your choice?"
    bot.send_message(chat_id=cid, text=text, reply_markup=reply_markup)


@run_async
def UserKeyboard(bot, update):

    custom_keyboard = [["/help"], ["/random"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    cid = update.message.chat.id
    text = "Welcome, use the /random to see a random picture from @titswiki."
    bot.send_message(chat_id=cid, text=text, reply_markup=reply_markup)


def DeleteSameValueOrNot(bot, update):

    text = (
        "<b>Do you want to delete the same value?</b>\n"
        "/DeleteSame\n")

    update.message.reply_text(
        text=text, parse_mode=ParseMode.HTML)


def PraiseListDelay(update):

    user_id = update.message.from_user.id
    if user_id not in config.PRAISE_LIST:
        config.PRAISE_LIST.append(user_id)
        return 0
    else:
        return 1


def FillList(in_list):

    if len(in_list) < config.FIVE_TYPE_LIST_MAX_LENGTH:
        if len(in_list) > config.FIVE_TYPE_LIST_MIN_LENGTH:
            in_list.append("None")
            FillList(in_list)
        else:
            raise Exception
    else:
        return in_list


@run_async
def invalid_command(bot, update):
    # text = "This command is invalid"
    # update.message.reply_text(text=text, quote=True)
    pass


def only_admin(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.message.from_user.id not in config.ADMINS:
            #invalid_command(bot, update, *args, **kwargs)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped
