#!/usr/bin/env python3

from telegram import InputMedia, InputMediaPhoto, InputMediaVideo
from telegram.ext import DispatcherHandlerStop
from telegram import ChatAction
from telegram import ParseMode

from hatsunebot import config
from hatsunebot.utils import full_list
from hatsunebot import error_log
from hatsunebot import sql

"""
{
    'message': {
        'forward_from_message_id': 20464,
        'delete_chat_photo': False,
        'date': 1534643,
        'caption_entities': [],
        'supergroup_chat_created': False,
        'new_chat_photo': [],
        'photo': [
            {
                'file_size': 1218,
                'width': 60,
                'height': 90,
                'file_id': 'AgADBQADF6gxG6docVf48DGahTHTOF891jIABAPn41l_BangI60CAAEC'
            },
            {
                'file_size': 15945,
                'width': 213,
                'height': 320,
                'file_id': 'AgADBQADF6gxG6docVf48DGahTHTOF891jIABKovc_9I66n2JK0CAAEC'
            },
            {
                'file_size': 88023,
                'width': 533,
                'height': 800,
                'file_id': 'AgADBQADF6gxG6docVf48DGahTHTOF891jIABF2R5PUSDbRpJa0CAAEC'
            },
            {
                'file_size': 108768,
                'width': 682,
                'height': 1024,
                'file_id': 'AgADBQADF6gxG6docVf48DGahTHTOF891jIABMtpmQhMmLRzIq0CAAEC'
            }
        ],
        'from': {
            'language_code': '',
            'is_bot': False,
            'username':'Floe',
            'id': 36,
            'first_name':'Flr'
        },
        'forward_from_chat': {
            'username': 't',
            'type': 'channel',
            'title': '~',
            'id': -01
        },
        'group_chat_created': False,
        'chat': {
            'first_name': 'Fler',
            'username': 'Fl',
            'type': 'private',
            'id': 380
        },
        'forward_date': 1563370,
        'channel_chat_created': False,
        'entities': [],
        'media_group_id': '1253861',
        'new_chat_members': [],
        'message_id': 395
    },
    'update_id': 306
}
"""


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
    """
    MESSAGE_ID, FROM_CHAT_ID
    [
        [3991, 366039180, 'AgADBQADHqgxG6docVevwzHBji_opA801TIABAqGbUg-S8HFP8ECAAEC'],
        [3991, 366039180, 'AgADBQADHqgxG6docVevwzHBji_opA801TIABFLydOubQv-6QMECAAEC'],
        [3991, 366039180, 'AgADBQADHqgxG6docVevwzHBji_opA801TIABPcr_ZfuycSkQcECAAEC'],
        [3991, 366039180, 'AgADBQADHqgxG6docVevwzHBji_opA801TIABAcJOOcyQWj8PsECAAEC'],
        [3992, 366039180, 'AgADBQADH6gxG6docVcHRcI6L68KiLRK1TIABIypPaslbU-akLICAAEC'],
        [3992, 366039180, 'AgADBQADH6gxG6docVcHRcI6L68KiLRK1TIABORRdKr0KXgRkbICAAEC'],
        [3992, 366039180, 'AgADBQADH6gxG6docVcHRcI6L68KiLRK1TIABAt95ny_A6KmkrICAAEC'],
        [3992, 366039180, 'AgADBQADH6gxG6docVcHRcI6L68KiLRK1TIABHhZdVsgP_YDj7ICAAEC'],
        [3993, 366039180, 'AgADBQADIKgxG6docVdP_5qOFLTLuk-p1jIABBgKpuOY0jmrxTkBAAEC'],
        [3993, 366039180, 'AgADBQADIKgxG6docVdP_5qOFLTLuk-p1jIABOQB-N1TfaNgxjkBAAEC'],
        [3993, 366039180, 'AgADBQADIKgxG6docVdP_5qOFLTLuk-p1jIABLYJfkdL-oupxDkBAAEC']
    ]
    """
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
            mid = tmp_list[0]
            file_id_1 = tmp_list[2]
            file_id_2 = tmp_list[3]
            file_id_3 = tmp_list[4]

            result_list = sql.check_sql_existed(
                mid, file_id_1, file_id_2, file_id_3)

            text = 'message_id:\n{0}:{1}\nfile_id_1:\n{2}:{3}\nfile_id_2:\n{4}:{5}\nfile_id_3:\n{6}:{7}\n'.format(
                    mid, result_list[0], file_id_1, result_list[1], file_id_2, result_list[2], file_id_3, result_list[3])
            update.message.reply_text(text=text, quote=True)
        else:
            config.SQL_LIST.append(tmp_list)
            config.FIVE_TYPE_LIST.append(tmp_list)

    # sql.process_sql(db, tmp_list)
    # sql.commit_mysql(db)
    # sql.close_mysql(db)

#     media_group_id = update.message.media_group_id
#     if media_group_i not in config.ALBUM_DICT:
#         bot.sendChatAction(
#             chat_id=update.message.from_user.id,
#             action=ChatAction.UPLOAD_PHOTO if update.message.photo else ChatAction.UPLOAD_VIDEO
#         )
#         config.ALBUM_DICT[media_group_id] = [update]
#         # schedule the job
#         job_queue.run_once(send_album, 1, context=[media_group_id])
#     else:
#         config.ALBUM_DICT[media_group_id].append(update)
#
#
# def send_album(bot, job):
#     media_group_id = job.context[0]
#     updates = config.ALBUM_DICT[media_group_id]
#
#     # delete from ALBUM_DICT
#     del config.ALBUM_DICT[media_group_id]
#
#     # ordering album updates
#     updates.sort(key=lambda x: x.message.message_id)
#
#     media = []
#     for update in updates:
#         if update.message.photo:
#             media.append(
#                 InputMediaPhoto(
#                     media=update.message.photo[-1].file_id,
#                     caption='' if update.message.caption is None else update.message.caption_html,
#                     parse_mode=ParseMode.HTML
#                 )
#             )
#         elif update.message.video:
#             media.append(
#                 InputMediaVideo(
#                     media=update.message.video.file_id,
#                     caption='' if update.message.caption is None else update.message.caption_html,
#                     parse_mode=ParseMode.HTML
#                 )
#             )
#     bot.sendMediaGroup(
#         chat_id=updates[0].message.from_user.id,
#         media=media
#     )
