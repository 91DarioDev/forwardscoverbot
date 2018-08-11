#!/usr/bin/env python3

from telegram import InputMedia, InputMediaPhoto, InputMediaVideo
from telegram.ext import DispatcherHandlerStop
from telegram import ChatAction
from telegram import ParseMode


ALBUM_DICT = {}


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
    media_group_id = update.message.media_group_id
    if media_group_id not in ALBUM_DICT:
        bot.sendChatAction(
            chat_id=update.message.from_user.id,
            action=ChatAction.UPLOAD_PHOTO if update.message.photo else ChatAction.UPLOAD_VIDEO
        )
        ALBUM_DICT[media_group_id] = [update]
        # schedule the job
        job_queue.run_once(send_album, 1, context=[media_group_id])
    else:
        ALBUM_DICT[media_group_id].append(update)


def send_album(bot, job):
    media_group_id = job.context[0]
    updates = ALBUM_DICT[media_group_id]

    # delete from ALBUM_DICT
    del ALBUM_DICT[media_group_id]

    # ordering album updates
    updates.sort(key=lambda x: x.message.message_id)

    media = []
    for update in updates:
        if update.message.photo:
            media.append(
                InputMediaPhoto(
                    media=update.message.photo[-1].file_id,
                    caption='' if update.message.caption is None else update.message.caption_html,
                    parse_mode=ParseMode.HTML
                )
            )
        elif update.message.video:
            media.append(
                InputMediaVideo(
                    media=update.message.video.file_id,
                    caption='' if update.message.caption is None else update.message.caption_html,
                    parse_mode=ParseMode.HTML
                )
            )
    bot.sendMediaGroup(
        chat_id=updates[0].message.from_user.id,
        media=media
    )
