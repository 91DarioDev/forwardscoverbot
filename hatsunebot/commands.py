#!/usr/bin/env python3

import logging
import copy
import random

from hatsunebot.utils import only_admin
from hatsunebot.utils import UserKeyboard
from hatsunebot.utils import AdminKeyboard
# from hatsunebot import keyboards
from hatsunebot import messages
from hatsunebot import utils
from hatsunebot import config
from hatsunebot import sql
from hatsunebot import error_log
from pymysql import err

# from telegram import MessageEntity
from telegram import ParseMode
# from telegram import constants as t_consts
from telegram.ext.dispatcher import run_async
from telegram import TelegramError


@run_async
@only_admin
def Command_Show(bot, update):

    # keyboard = keyboards.github_link_kb()

    AdminKeyboard(bot, update)

    sql_status_list = sql.SQL_ShowStatus()
    # now we make the string about the sql status
    sql_status_str = ''
    if len(sql_status_list) != 0:
        for s in sql_status_list:
            sql_status_str = sql_status_str + \
                str(s[0]) + ': ' + str(s[1]) + '\n'

    text = (
        "<b>Hatsune' Telegram Bot Guide:</b>."
        "\n<i>It works also if you edit messages or forward messages. "
        "It also keeps the same text formatting style.</i>\n\n"
        "<b>MySQL Status:</b>\n"
        "{0}\n"
        "<b>MySQL Tables Detail:</b>\n"
        "{1}\n"
        "<b>Forward Status:</b>\n"
        "{2}\n"
        "<b>Check Status:</b>\n"
        "{3}\n".format(str(config.SQL_STATUS),
                       str(sql_status_str),
                       str(config.FORWARD_STATUS),
                       str(config.CHECK_STATUS))
    )
    # update.message.reply_text(
    #     text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    update.message.reply_text(
        text=text, parse_mode=ParseMode.HTML)


@run_async
def Command_UserHelpShow(bot, update):

    UserKeyboard(bot, update)
    if utils.PraiseListDelay(update) == 1:
        text = "_(√ ζ ε:)_"
        update.message.reply_text(
            text=text, parse_mode=ParseMode.HTML)
        return
    text = (
        "<b>PicBot:</b>."
        "\n<i>See the titswiki random photo from begin to now.</i>\n\n"
        "Use command:\n"
        "-> /random\n"
    )
    # update.message.reply_text(
    #     text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    update.message.reply_text(
        text=text, parse_mode=ParseMode.HTML)


@run_async
@only_admin
def Command_CheckAllData(bot, update):
    '''
    check all the data in MySQL and delete the same value
    '''

    text = "<b>Start Checking...</b>"
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

    # check all the data in mysql
    db = sql.SQL_ConnectMysql()

    sql.SQL_GetMaxTableCount()

    for table_id in range(0, config.NU_RANDOM):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, table_id)

        try:
            r_rows = -1
            same_file_id_value_list = sql.SQL_IterationAllData(
                db, table_name, update)
        except Exception as e:
            if r_rows != -1:
                e = 'CheckAllData() get mid failed: ' + str(e.args) + ': r_rows: ' + str(r_rows)
                error_log.RecordError(e)
            else:
                e = 'CheckAllData() get mid failed: ' + str(e.args)
                error_log.RecordError(e)

            return

    i_text = '\n\n'
    i = 0
    for s in config.CHECK_FILE_ID_LIST:
        i_text = i_text + str(s) + ': ' + \
            str(same_file_id_value_list[i]) + '\n'
        i += 1

    text = (
        "<b>Check Result:</b>."
        "\n<i>Found:</i>\n\n"
        "SameFileID: %s"
        "<i>Now this program will auto delete the same value...</i>" % (i_text)
    )
    # update.message.reply_text(
    #     text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    update.message.reply_text(
        text=text, parse_mode=ParseMode.HTML)

    COPY_LIST = copy.deepcopy(config.CHECK_FILE_ID_LIST)

    for f in COPY_LIST:
        sql.SQL_DeleteSameValue(f)
        try:
            config.CHECK_FILE_ID_LIST.pop(0)
        except IndexError as e:
            e = 'CheckAllData() del failed' + str(e.args) + ' ---> ' + str(COPY_LIST)
            error_log.RecordError(e)

    text = "<b>OK</b>"
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
    sql.SQL_Close(db)


@run_async
def Command_CallBackQueryMid(bot, job):

    sql.SQL_GetMaxTableCount()
    table_id = random.randint(0, config.NU_RANDOM - 1)
    table_name = "{0}pic_{1}".format(config.SQL_FORMAT, table_id)
    print(table_name)
    status = -1
    while status == -1:
        status = sql.SQL_GetMidLimited(table_name)



def Command_CallBackQueryMid_Fix():

    table_id = random.randint(0, config.NU_RANDOM - 1)
    table_name = "{0}pic_{1}".format(config.SQL_FORMAT, table_id)
    status = -1
    while status == -1:
        status = sql.SQL_GetMidLimited(table_name)


@run_async
def Command_RandomPicShow(bot, update):

    # we have to
    if update.message.from_user.is_bot == 'True':
        return

    error_log.RecordError("RandomPicShow()")
    table_id = 0
    fid = None

    mid_random = random.randint(0, config.MAX_MID_LIST - 1)
    while len(config.MID_LIST) == 0:
        error_log.RecordError("RandomPicShow() mid")
        Command_CallBackQueryMid_Fix()
    mid = config.MID_LIST[0][mid_random][0]
    error_log.RecordError("RandomPicShow() mid [%s]" % mid)

    while fid == None and table_id < config.NU_RANDOM and table_id >= 0:
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, table_id)
        print(table_name)
        try:
            fid = sql.SQL_GetFid(table_name, mid)
            error_log.RecordError("RandomPicShow() fid [%s]" % fid)
            table_id += 1
        except err.InterfaceError:
            error_log.RecordError(
                "RandomPicShow() err.InterfaceError - table name [%s] fid[%s]" % (table_name, fid))

    #print(mid, fid)
    error_log.RecordError("RandomPicShow() mid[%s] - fid[%s]" % (mid, fid))

    cid = update.message.chat.id
    try:
        bot.forwardMessage(
            chat_id=cid, from_chat_id=fid, message_id=mid)
    except TelegramError as e:
        e = 'RandomPicShow() ForwardMessage failed: ' + str(e.args)
        error_log.RecordError(e)


@run_async
@only_admin
def Command_DeleteSame(bot, update):

    if config.CHECK_STATUS == False:

        text = "Error, you are not in check status\n"
        update.message.reply_text(text=text, quote=True)

    else:

        COPY_LIST = copy.deepcopy(config.CHECK_FILE_ID_LIST)
        for d in COPY_LIST:
            sql.SQL_DeleteSameValue(d)
            try:
                # del config.CHECK_FILE_ID_LIST[0]
                config.CHECK_FILE_ID_LIST.pop(0)
            except IndexError as e:
                e = 'CallBack_SQL() del failed' + str(e.args) + ' ---> ' + str(COPY_LIST)
                error_log.RecordError(e)

        text = "<b>OK, deleting the same value now</b>"
        update.message.reply_text(text=text, parse_mode=ParseMode.HTML)


@run_async
@only_admin
def Command_ShowCheckResult(bot, update):

    if config.CHECK_SHOW == True:

        config.CHECK_SHOW = False
        text = "<b>OK, stop show</b>"
        update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

    else:

        config.CHECK_SHOW = True
        text = "<b>OK, start show</b>"
        update.message.reply_text(text=text, parse_mode=ParseMode.HTML)


@run_async
@only_admin
def Command_CheckExistedOrNot(bot, update):

    # if the config.CHECK_STATUS is True
    # bot will not processed the photo message and insert into MySQL
    if config.CHECK_STATUS == False:

        config.CHECK_STATUS = True

        # remember this is cid
        # config.CHECK_REPLY_CID = update.message.chat.id

        text = "<b>OK, send me a photo to check existed or not</b>"
        update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

    else:

        config.CHECK_STATUS = False
        text = "<b>OK, turn off the check</b>"
        update.message.reply_text(text=text, parse_mode=ParseMode.HTML)


@run_async
def Command_CallBackSQL(bot, job):

    # deep copy the list of SQL_LIST
    # then we delete is one by one
    # COPY_LIST = [[MESSAGE_ID, FROM_CHAT_ID， FILE_ID_1, FILE_ID_2, FILE_ID_3], [MESSAGE_ID, FROM_CHAT_ID, FILE_ID, FILE_ID_2, FILE_ID_3]]
    if config.SQL_STATUS == False:
        return

    COPY_LIST = copy.deepcopy(config.SQL_LIST)
    if len(COPY_LIST) == 0:
        return
    db = sql.SQL_ConnectMysql()
    for c in COPY_LIST:
        sql.SQL_Process(db, c)
        try:
            # del config.SQL_LIST[0]
            config.SQL_LIST.pop(0)
        except IndexError as e:
            e = 'CallBack_SQL() del failed' + str(e.args) + ' ---> \n' + \
                str(COPY_LIST) + ' ---> \n' + str(config.SQL_LIST)
            error_log.RecordError(e)
    sql.SQL_Commit(db)
    sql.SQL_Close(db)


@run_async
def Command_Clean():
    '''
    make the LAST_MESSAGE_ID_LIST none
    '''

    # print(config.LAST_MESSAGE_ID_LIST)
    config.LAST_MESSAGE_ID_LIST = []


@run_async
def Command_DeleteOnePraiseListItem(bot, job):
    '''
    delete one in the praise
    '''

    if len(config.PRAISE_LIST) != 0:
        config.PRAISE_LIST.pop(0)


@run_async
def Command_CallBackAutoSend(bot, job):
    '''
    send the photo by timeI
    '''

    if config.CHECK_STATUS == True:
        # if that
        # we do something here then just return
        return

    if config.FORWARD_STATUS == False:
        config.FIVE_TYPE_LIST = []
        return

    try:
        COPY_LIST = copy.deepcopy(config.FIVE_TYPE_LIST)
        # file_id = config.PHOTO_FILE_ID[0]
    except IndexError:
        return

    if COPY_LIST is None:
        return

    for five_type_list in COPY_LIST:
        mid = five_type_list[0]
        fid = five_type_list[1]

        # init the LAST_MESSAGE_ID
        # the same as if len(list) == 0 but below is better
        if not config.LAST_MESSAGE_ID_LIST:
            config.LAST_MESSAGE_ID_LIST.append(str(mid))

            for cid in config.CHAT_ID:
                # only send one pic once
                # bot.send_photo(chat_id=cid, photo=file_id, caption=None)
                try:
                    bot.forwardMessage(
                        chat_id=cid, from_chat_id=fid, message_id=mid)
                except TelegramError as e:
                    e = 'callback_minute_send() ForwardMessage failed: ' + str(e.args) + \
                        ' ---> ' + str(fid) + ', ' + str(mid)
                    error_log.RecordError(e)
                    # pass
            # del config.PHOTO_FILE_ID[0]
            try:
                # error_config_list = copy.deepcopy(config.FIVE_TYPE_LIST)
                # del config.FIVE_TYPE_LIST[0]
                config.FIVE_TYPE_LIST.pop(0)
            except IndexError as e:
                e = 'callback_minute_send() del failed: ' + str(e.args) + \
                    ' ---> ' + str(config.FIVE_TYPE_LIST)
                error_log.RecordError(e)
                # pass
        # check the same message_id and pass
        else:
            if mid not in config.LAST_MESSAGE_ID_LIST:
                for cid in config.CHAT_ID:
                    # only send one pic once
                    # bot.send_photo(chat_id=cid, photo=file_id, caption=None)
                    try:
                        bot.forwardMessage(
                            chat_id=cid, from_chat_id=fid, message_id=mid)
                        config.LAST_MESSAGE_ID_LIST.append(str(mid))
                    except Exception as e:
                        e = 'callback_minute_send() ForwardMessage failed: ' + str(e.args) + \
                            ' ---> ' + str(fid) + ', ' + str(mid)
                        error_log.RecordError(e)
                        pass
                try:
                    # error_config_list = copy.deepcopy(config.FIVE_TYPE_LIST)
                    # del config.FIVE_TYPE_LIST[0]
                    config.FIVE_TYPE_LIST.pop(0)
                except Exception as e:
                    e = 'callback_minute_send() del failed: ' + str(e.args) + \
                        ' ---> ' + str(config.FIVE_TYPE_LIST)
                    error_log.RecordError(e)
                    pass

    Command_Clean()


@run_async
@only_admin
def Command_ForwardStateTransition(bot, update):

    if config.FORWARD_STATUS == False:
        config.FORWARD_STATUS = True
        text = "<b>Forward enabled</b>"
        update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

    elif config.FORWARD_STATUS == True:
        config.FORWARD_STATUS = False
        text = "<b>Forward disabled</b>"
        update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
