#!/usr/bin/env python3

from hatsunebot import constants

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def github_link_kb():
    button0 = InlineKeyboardButton(
        text="Source code",
        url="https://github.com/rikonaka/forwards-pics-bot.git")
    buttons_list = [[button0]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def private_chat_kb():
    bot_link = "https://t.me/{}".format(constants.GET_ME.username)
    button0 = InlineKeyboardButton(text="Private chat", url=bot_link)
    buttons_list = [[button0]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard
