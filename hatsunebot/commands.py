#!/usr/bin/env python3

import logging
import copy
import random

from hatsunebot.utils import only_admin
from hatsunebot.utils import common_help
from hatsunebot.utils import admin_help
# from hatsunebot import keyboards
from hatsunebot import messages
from hatsunebot import config
from hatsunebot import sql
from hatsunebot import error_log

# from telegram import MessageEntity
from telegram import ParseMode
# from telegram import constants as t_consts
from telegram.ext.dispatcher import run_async
from telegram import TelegramError


@run_async
@only_admin
def help_command(bot, update):

    # keyboard = keyboards.github_link_kb()

    admin_help(bot, update)

    sql_status_list = sql.show_sql_status()
    # now we make the string about the sql status
    sql_status_str = ''
    if len(sql_status_list) != 0:
        for s in sql_status_list:
            # [table_name(char), rows(int)]
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
                       sql_status_str,
                       str(config.FORWARD_STATUS),
                       str(config.CHECK_STATUS))
        # "\n<b>Supported commands(Only for admin):</b>\n\n"
        # "/Show\n\n"
        # "/turn_off_sql\n\n"
        # "/turn_on_sql\n\n"
        # "/StopForward\n\n"
        # "/StartForward\n\n"
        # "/ForwardStateTransition\n\n"
        # "/CheckExistedOrNot\n\n"
        # "/CheckResultShow\n\n"
        # "/CheckAllData\n\n"
    )
    # update.message.reply_text(
    #     text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    update.message.reply_text(
        text=text, parse_mode=ParseMode.HTML)


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
@only_admin
def check_all_data(bot, update):
    '''
    check all the data in MySQL and delete the same value
    '''

    text = "<b>Start Checking...</b>"
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

    # check all the data in mysql
    db = sql.connect_mysql()

    sql.get_max_tables()

    for table_id in range(0, config.NU_RANDOM):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, table_id)

        try:
            r_rows = -1
            same_file_id_value_list = sql.iteration_all_data(
                db, table_name, update)
        except Exception as e:
            if r_rows != -1:
                e = 'check_all_data() get mid failed: ' + str(e.args) + ': r_rows: ' + str(r_rows)
                error_log.write_it(e)
            else:
                e = 'check_all_data() get mid failed: ' + str(e.args)
                error_log.write_it(e)

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
        sql.delete_same_value(f)
        try:
            config.CHECK_FILE_ID_LIST.pop(0)
        except IndexError as e:
            e = 'check_all_data() del failed' + str(e.args) + ' ---> ' + str(COPY_LIST)
            error_log.write_it(e)

    text = "<b>OK</b>"
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
    sql.close_mysql(db)


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
        r_rows = -1
        mid, r_rows = sql.random_pick_mid(db, table_name)
    except Exception as e:
        if r_rows != -1:
            e = 'random_pic() get mid failed: ' + str(e.args) + ': r_rows: ' + str(r_rows)
            error_log.write_it(e)
        else:
            e = 'random_pic() get mid failed: ' + str(e.args)
            error_log.write_it(e)

        sql.close_mysql(db)
        random_pic(bot, update)
        # text = "..."
        # update.message.reply_text(text=text, quote=True)
        # sql.close_mysql(db)
        return

    try:
        fid = sql.select_fid(db, table_name, mid)
    except Exception as e:
        e = 'random_pic() get fid failed: ' + str(e.args)
        error_log.write_it(e)
        sql.close_mysql(db)
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
    except TelegramError as e:
        e = 'random_pic() ForwardMessage failed: ' + str(e.args)
        error_log.write_it(e)
        # pass

    sql.close_mysql(db)


@run_async
@only_admin
def delete_same(bot, update):

    if config.CHECK_STATUS == False:

        text = "Error, you are not in check status\n"
        update.message.reply_text(text=text, quote=True)

    else:

        COPY_LIST = copy.deepcopy(config.CHECK_FILE_ID_LIST)
        for d in COPY_LIST:
            sql.delete_same_value(d)
            try:
                # del config.CHECK_FILE_ID_LIST[0]
                config.CHECK_FILE_ID_LIST.pop(0)
            except IndexError as e:
                e = 'callback_sql() del failed' + str(e.args) + ' ---> ' + str(COPY_LIST)
                error_log.write_it(e)

        text = "<b>OK, deleting the same value now</b>"
        update.message.reply_text(text=text, parse_mode=ParseMode.HTML)


@run_async
@only_admin
def check_result_show(bot, update):

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
def check_existed(bot, update):

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
        try:
            # del config.SQL_LIST[0]
            config.SQL_LIST.pop(0)
        except IndexError as e:
            e = 'callback_sql() del failed' + str(e.args) + ' ---> \n' + \
                str(COPY_LIST) + ' ---> \n' + str(config.SQL_LIST)
            error_log.write_it(e)
    sql.commit_mysql(db)
    sql.close_mysql(db)


def clean_up():
    '''
    make the LAST_MESSAGE_ID_LIST none
    '''

    # print(config.LAST_MESSAGE_ID_LIST)
    config.LAST_MESSAGE_ID_LIST = []


# send here
@run_async
def callback_minute_send(bot, job):
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
                    error_log.write_it(e)
                    # pass
            # del config.PHOTO_FILE_ID[0]
            try:
                # error_config_list = copy.deepcopy(config.FIVE_TYPE_LIST)
                # del config.FIVE_TYPE_LIST[0]
                config.FIVE_TYPE_LIST.pop(0)
            except IndexError as e:
                e = 'callback_minute_send() del failed: ' + str(e.args) + \
                    ' ---> ' + str(config.FIVE_TYPE_LIST)
                error_log.write_it(e)
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
                        error_log.write_it(e)
                        pass
                try:
                    # error_config_list = copy.deepcopy(config.FIVE_TYPE_LIST)
                    # del config.FIVE_TYPE_LIST[0]
                    config.FIVE_TYPE_LIST.pop(0)
                except Exception as e:
                    e = 'callback_minute_send() del failed: ' + str(e.args) + \
                        ' ---> ' + str(config.FIVE_TYPE_LIST)
                    error_log.write_it(e)
                    pass

    clean_up()


@run_async
@only_admin
def forward_state_transition(bot, update):

    if config.FORWARD_STATUS == False:
        config.FORWARD_STATUS = True
        text = "<b>Forward enabled</b>"
        update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

    elif config.FORWARD_STATUS == True:
        config.FORWARD_STATUS = False
        text = "<b>Forward disabled</b>"
        update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
