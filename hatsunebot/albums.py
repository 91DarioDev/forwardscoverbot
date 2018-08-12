#!/usr/bin/env python3

from telegram import InputMedia, InputMediaPhoto, InputMediaVideo
from telegram.ext import DispatcherHandlerStop
from telegram import ChatAction
from telegram import ParseMode

from hatsunebot import config
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
            'username':
            'Floe',
            'id': 36,
            'first_name':
            'Flr'
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
    db = sql.connect_mysql()
    for f in update.message.photo:
        file_id = f.file_id
        sql.process_sql(db, file_id)
        config.PHOTO_FILE_ID.append(file_id)

    sql.commit_mysql(db)
    sql.close_mysql(db)

#     media_group_id = update.message.media_group_id
#     if media_group_i not in config.ALBUM_DICT:
#         bot.sendChatAction(
#             chat_id=update.message.from_user.id,
#             action=ChatAction.UPLOAD_PHOTO if update.message.photo else ChatAction.UPLOAD_VIDEO
#         )
#         config.ALBUM_DICT[media_group_id] = [update]
#         schedule the job
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
#
