#!/usr/bin/env python3

import logging
import copy

from hatsunebot.utils import only_admin
# from hatsunebot import keyboards
from hatsunebot import messages
from hatsunebot import config
from hatsunebot import sql

# from telegram import MessageEntity
from telegram import ParseMode
# from telegram import constants as t_consts
from telegram.ext.dispatcher import run_async


@run_async
def random_pic(bot, update):

    db = sql.connect_mysql()
    try:
        mid, fid = sql.random_pick_from_mysql(db)
    except TypeError:
        text = "..."
        update.message.reply_text(text=text, quote=True)
        sql.close_mysql(db)
        return
    # print("2: {0} {1}".format(mid, fid))

    # logging.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # logging.debug(file_id)
    for cid in config.CHAT_ID:
        if config.FORWARD_STATUS == True:
            # bot.send_photo(chat_id=cid, photo=file_id, caption=None)
            bot.forwardMessage(
                chat_id=cid, from_chat_id=fid, message_id=mid)

    sql.close_mysql(db)


@run_async
@only_admin
def help_command(bot, update):

    # keyboard = keyboards.github_link_kb()
    text = (
        "<b>Hatsune' Telegram Bot Guide:</b>."
        "\n<i>It works also if you edit messages or forward messages. "
        "It also keeps the same text formatting style.</i>\n\n"
        "<b>Supported commands(Only for admin):</b>\n"
        "/turn_off_sql\n"
        "/turn_on_sql\n"
        "/stop_forward\n"
        "/start_forward\n"
    )
    # update.message.reply_text(
    #     text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    update.message.reply_text(
        text=text, parse_mode=ParseMode.HTML)


@run_async
def callback_sql(bot, job):

    # deep copy the list of SQL_LIST
    # then we delete is one by one
    # COPY_LIST = [[MESSAGE_ID, FROM_CHAT_ID， FILE_ID_1, FILE_ID_2, FILE_ID_3], [MESSAGE_ID, FROM_CHAT_ID, FILE_ID, FILE_ID_2, FILE_ID_3]]
    COPY_LIST = copy.deepcopy(config.SQL_LIST)
    db = sql.connect_mysql()
    for c in COPY_LIST:
        sql.process_sql(db, c)
        del config.SQL_LIST[0]
    sql.commit_mysql(db)
    sql.close_mysql(db)

# send here


@run_async
def callback_minute_send(bot, job):

    try:
        three_type = config.FIVE_TYPE_LIST[0]
        # file_id = config.PHOTO_FILE_ID[0]
    except IndexError:
        return
    mid = three_type[0]
    fid = three_type[1]
    for cid in config.CHAT_ID:
        # only send one pic once
        if config.FORWARD_STATUS == True:
            # bot.send_photo(chat_id=cid, photo=file_id, caption=None)
            bot.forwardMessage(
                chat_id=cid, from_chat_id=fid, message_id=mid)

    # del config.PHOTO_FILE_ID[0]
    del config.FIVE_TYPE_LIST[0]

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
        text = ("Turn off sql record done")
        update.message.reply_text(text=text)
    return


@run_async
@only_admin
def turn_on_sql(bot, update):

    if config.SQL_STATUS == True:
        pass
    else:
        config.SQL_STATUS = True
        text = ("Turn on sql record done")
        update.message.reply_text(text=text)
    return


@run_async
@only_admin
def stop_forward(bot, update):

    if config.FORWARD_STATUS == False:
        pass
    else:
        config.FORWARD_STATUS = False
        text = ("Stop forward now")
        update.message.reply_text(text=text)
    return


@run_async
@only_admin
def start_forward(bot, update):

    if config.FORWARD_STATUS == True:
        pass
    else:
        config.SQL_STATUS = True
        text = ("Start forward now")
        update.message.reply_text(text=text)
    return
