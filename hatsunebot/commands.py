#!/usr/bin/env python3

from hatsunebot.utils import only_admin
from hatsunebot import keyboards
from hatsunebot import messages
from hatsunebot import config

# from telegram import MessageEntity
from telegram import ParseMode
# from telegram import constants as t_consts
from telegram.ext.dispatcher import run_async


@run_async
@only_admin
def help_command(bot, update):

    keyboard = keyboards.github_link_kb()
    text = (
        "<b>Hatsune' Telegram Bot Guide:</b>."
        "\n<i>It works also if you edit messages or forward messages. "
        "It also keeps the same text formatting style.</i>\n\n"
        "<b>Supported commands(Only for admin):</b>\n"
        "/turn_off_sql\n"
        "/turn_on_sql\n"
    )
    update.message.reply_text(
        text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


# send here
@run_async
def callback_minute(bot, job):

    try:
        for cid in config.CHAT_ID:
            file_id = config.PHOTO_FILE_ID[0]
            bot.send_photo(chat_id=cid, photo=file_id, caption=None)
            del config.PHOTO_FILE_ID[0]
    except IndexError:
        pass

    # try:
    #     mid = config.MESSAGE_ID_LIST[0]
    #     fid = config.FROM_CHAT_ID_LIST[0]
    # except IndexError:
    #     return
    # bot.send_message(chat_id=config.CHAT_ID, text=send_message)
    # for c in config.CHAT_ID:
    #     bot.forwardMessage(chat_id=c, from_chat_id=fid, message_id=mid)

    # del config.MESSAGE_ID_LIST[0]
    # del config.FROM_CHAT_ID_LIST[0]


@run_async
@only_admin
def turn_off_sql(bot, update):

    if config.SQL_STATUS == False:
        pass
    else:
        config.SQL_STATUS = False
        text = ("Turn off sql done")
        update.message.reply_text(text=text)
    return


@run_async
@only_admin
def turn_on_sql(bot, update):

    if config.SQL_STATUS == True:
        pass
    else:
        config.SQL_STATUS = True
        text = ("Turn on sql done")
        update.message.reply_text(text=text)
    return
