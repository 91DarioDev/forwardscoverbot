#!/usr/bin/env python3

import logging
import copy
import random

from hatsunebot.utils import only_admin
from hatsunebot.utils import common_help
# from hatsunebot import keyboards
from hatsunebot import messages
from hatsunebot import config
from hatsunebot import sql

# from telegram import MessageEntity
from telegram import ParseMode
# from telegram import constants as t_consts
from telegram.ext.dispatcher import run_async
from telegram import error


@run_async
def common_help_show(bot, update):

    common_help(bot, update)
    text = (
        "<b>PicBot Guide:</b>."
        "\n<i>See the titswiki random photo from begin to now.</i>\n\n"
    )
    # update.message.reply_text(
    #     text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    update.message.reply_text(
        text=text, parse_mode=ParseMode.HTML)


@run_async
def random_pic(bot, update):

    # we have to
    if update.message.from_user.is_bot == True:
        return
    db = sql.connect_mysql()

    sql.get_max_tables()
    table_id = random.randint(0, config.NU_RANDOM)
    table_name = "{0}pic_{1}".format(config.SQL_FORMAT, table_id)
    try:
        mid = sql.random_pick_mid(db, table_name)
    except Exception:
        random_pic(bot, update)
        # text = "..."
        # update.message.reply_text(text=text, quote=True)
        # sql.close_mysql(db)
        return

    try:
        fid = sql.select_fid(db, table_name, mid)
    except Exception:
        random_pic(bot, update)
        # text = "..."
        # update.message.reply_text(text=text, quote=True)
        # sql.close_mysql(db)
        return

    # print("++++++++++++++++++++{}".format(mid))
    # print("++++++++++++++++++++{}".format(fid))
    # for cid in config.CHAT_ID:
        # bot.send_photo(chat_id=cid, photo=file_id, caption=None)
    cid = update.message.chat.id
    try:
        # print(fid)
        # print(mid)
        bot.forwardMessage(
            chat_id=cid, from_chat_id=fid, message_id=mid)
    except error.TimedOut:
        pass

    sql.close_mysql(db)


@run_async
@only_admin
def help_command(bot, update):

    # keyboard = keyboards.github_link_kb()
    text = (
        "<b>Hatsune' Telegram Bot Guide:</b>."
        "\n<i>It works also if you edit messages or forward messages. "
        "It also keeps the same text formatting style.</i>\n\n"
        "<b>MySQL Status:</b>\n"
        "{0}\n"
        "<b>Forward Status:</b>\n"
        "{1}\n"
        "\n<b>Supported commands(Only for admin):</b>\n\n"
        "/show\n\n"
        "/turn_off_sql\n\n"
        "/turn_on_sql\n\n"
        "/stop_forward\n\n"
        "/start_forward\n\n".format(str(config.SQL_STATUS),
                                    str(config.FORWARD_STATUS))
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
    if config.SQL_STATUS == False:
        return

    COPY_LIST = copy.deepcopy(config.SQL_LIST)
    if len(COPY_LIST) == 0:
        return
    db = sql.connect_mysql()
    for c in COPY_LIST:
        sql.process_sql(db, c)
        del config.SQL_LIST[0]
    sql.commit_mysql(db)
    sql.close_mysql(db)

# send here


@run_async
def callback_minute_send(bot, job):

    if config.FORWARD_STATUS == False:
        config.FIVE_TYPE_LIST = []
        return

    try:
        five_type = config.FIVE_TYPE_LIST[0]
        # file_id = config.PHOTO_FILE_ID[0]
    except IndexError:
        return

    if five_type is None:
        return
    mid = five_type[0]
    fid = five_type[1]
    for cid in config.CHAT_ID:
        # only send one pic once
        # bot.send_photo(chat_id=cid, photo=file_id, caption=None)
        try:
            bot.forwardMessage(
                chat_id=cid, from_chat_id=fid, message_id=mid)
        except error.BadRequest:
            pass

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
        config.FORWARD_STATUS = True
        text = ("Start forward now")
        update.message.reply_text(text=text)
    return
