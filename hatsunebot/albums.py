#!/usr/bin/env python3

from telegram import InputMedia, InputMediaPhoto, InputMediaVideo
from telegram.ext import DispatcherHandlerStop
from telegram import ChatAction
from telegram import ParseMode
from telegram.ext.dispatcher import run_async

from hatsunebot import config
from hatsunebot.utils import FillList
from hatsunebot.utils import DeleteSameValueOrNot
from hatsunebot.utils import PraiseListDelay
from hatsunebot import error_log
from hatsunebot import sql
from hatsunebot.utils import only_admin


@run_async
def CollectAlbum_User(bot, update, job_queue):
    '''
    design for the group normal users
    '''

    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message

    if message.photo:
        if PraiseListDelay(update) == 1:
            return
        # here we add the reply same words
        re_text = message.text_html
        # split the command message
        re_text = '好看~~ o(*￣▽￣*)ブ'
        message.reply_text(text=re_text, parse_mode=ParseMode.HTML)


@run_async
@only_admin
def CollectAlbum_Admin(bot, update, job_queue):
    '''
    design for the group admin user
    '''

    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message

    config.CONFLICT_LIST = []
    tmp_list = []

    message_id = message.message_id
    tmp_list.append(message_id)

    from_chat_id = message.chat.id
    tmp_list.append(from_chat_id)

    for f in message.photo:
        tmp_list.append(f.file_id)

    try:
        tmp_list = FillList(tmp_list)
    except Exception as e:
        e = 'CollectAlbum tmp_list failed: ' + str(e.args)
        error_log.RecordError(e)
        return

    if config.CHECK_STATUS == True:
        file_id_1 = tmp_list[2]
        file_id_2 = tmp_list[3]
        file_id_3 = tmp_list[4]

        result_list = sql.SQL_CheckExisted(
            file_id_1, file_id_2, file_id_3)

        if config.CHECK_SHOW == True:
            # more information
            text = 'file_id_1:\n{0}\nfile_id_2:\n{1}\nfile_id_3:\n{2}\n'.format(
                result_list[0], result_list[1], result_list[2])
            message.reply_text(text=text, quote=True)

        if result_list[0] == 0 and result_list[1] == 0 and result_list[2] == 0:
            config.SQL_LIST.append(tmp_list)
            text = 'This message is not include in MySQL, inserting...'
            message.reply_text(text=text, quote=True)

        elif result_list[0] > 1:
            text = 'file_id_1:\n{0}\nfile_id_2:\n{1}\nfile_id_3:\n{2}\n'.format(
                result_list[0], result_list[1], result_list[2])
            message.reply_text(text=text, quote=True)
            config.CHECK_FILE_ID_LIST.append(file_id_1)
            DeleteSameValueOrNot(bot, update)

    else:
        config.SQL_LIST.append(tmp_list)
        config.FIVE_TYPE_LIST.append(tmp_list)


@run_async
def CollectAlbum(bot, update, job_queue):
    '''
    if the media_group_id not a key in the dictionary yet:
        - send sending action
        - create a key in the dict with media_group_id
        - add a list to the key and the first element is this update
        - schedule a job in 1 sec
    else:
        - add update to the list of that media_group_id
    '''
    # now we append every file_id into list and sql
    if update.message.forward_from_chat:
        if update.message.forward_from_chat.username in config.ADMINS_GROUP:
            CollectAlbum_Admin(bot, update, job_queue)
            return
    # deal with the normal user's send
    CollectAlbum_User(bot, update, job_queue)
