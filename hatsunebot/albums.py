#!/usr/bin/env python3

from telegram import InputMedia, InputMediaPhoto, InputMediaVideo
from telegram.ext import DispatcherHandlerStop
from telegram import ChatAction
from telegram import ParseMode
from telegram.ext.dispatcher import run_async

from hatsunebot import config
from hatsunebot.utils import full_list
from hatsunebot.utils import delete_command
from hatsunebot import error_log
from hatsunebot import sql
from hatsunebot.utils import only_admin


@run_async
@only_admin
def collect_album_items(bot, update, job_queue):
    """
    if the media_group_id not a key in the dictionary yet:
        - send sending action
        - create a key in the dict with media_group_id
        - add a list to the key and the first element is this update
        - schedule a job in 1 sec
    else:
        - add update to the list of that media_group_id
    """
    # now we append every file_id into list and sql
    # FIVE_TYPE_LIST = [[MESSAGE_ID, FROM_CHAT_ID， FILE_ID_1, FILE_ID_2, FILE_ID_3], [MESSAGE_ID, FROM_CHAT_ID, FILE_ID_1, FILE_ID_2, FILE_ID_3]]
    if update.message.forward_from_chat:
        if update.message.forward_from_chat.username not in config.ADMINS_GROUP:
            return

    config.CONFLICT_LIST = []
    tmp_list = []

    message_id = update.message.message_id
    tmp_list.append(message_id)

    from_chat_id = update.message.chat.id
    tmp_list.append(from_chat_id)

    # db = sql.connect_mysql()
    for f in update.message.photo:
        tmp_list.append(f.file_id)

        # conflict check
        # media_group_id = update.message.media_group_id
    try:
        tmp_list = full_list(tmp_list)
    except Exception as e:
        e = 'collect_album_items tmp_list failed: ' + str(e.args)
        error_log.write_it(e)
        return

    if config.CHECK_STATUS == True:
        # config.CHECK_LIST.append(tmp_list)
        # mid = tmp_list[0]
        file_id_1 = tmp_list[2]
        file_id_2 = tmp_list[3]
        file_id_3 = tmp_list[4]

        result_list = sql.check_sql_existed(
            file_id_1, file_id_2, file_id_3)

        # text = 'file_id_1:\n{0}\nfile_id_2:\n{1}\nfile_id_3:\n{2}\n'.format(
        #     result_list[0], result_list[1], result_list[2])
        # update.message.reply_text(text=text, quote=True)

        if config.CHECK_SHOW == True:

            # more information
            text = 'file_id_1:\n{0}\nfile_id_2:\n{1}\nfile_id_3:\n{2}\n'.format(
                result_list[0], result_list[1], result_list[2])
            update.message.reply_text(text=text, quote=True)

        if result_list[0] == 0 and result_list[1] == 0 and result_list[2] == 0:

            config.SQL_LIST.append(tmp_list)
            text = 'This message is not include in MySQL, inserting...'
            update.message.reply_text(text=text, quote=True)

            # result_list = sql.check_sql_existed(
            #     file_id_1, file_id_2, file_id_3)
            # text = 'New: file_id_1:\n{0}\nfile_id_2:\n{1}\nfile_id_3:\n{2}\n'.format(
            #     result_list[0], result_list[1], result_list[2])
            # update.message.reply_text(text=text, quote=True)

        elif result_list[0] > 1:

            text = 'file_id_1:\n{0}\nfile_id_2:\n{1}\nfile_id_3:\n{2}\n'.format(
                result_list[0], result_list[1], result_list[2])
            update.message.reply_text(text=text, quote=True)
            config.CHECK_FILE_ID_LIST.append(file_id_1)
            delete_command(bot, update)

    else:
        config.SQL_LIST.append(tmp_list)
        config.FIVE_TYPE_LIST.append(tmp_list)