# ForwardsCoverBot - don't let people on telegram forward with your name on the forward label
# Copyright (C) 2017-2018  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
#
# ForwardsCoverBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ForwardsCoverBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with ForwardsCoverBot.  If not, see <http://www.gnu.org/licenses/>

from telegram import InputMedia, InputMediaPhoto, InputMediaVideo
from telegram.ext import DispatcherHandlerStop
from telegram import ChatAction
from telegram import ParseMode



ALBUM_DICT = {}


def possible_album_processing(bot, update, job_queue):
    if is_album(bot, update):
        collect_album_items(bot, update, job_queue)
        raise DispatcherHandlerStop
    else:
        return


def is_album(bot, update):
    """ 
    return True or False if the message is part of an album
    """
    if update.message.media_group_id is None:
        return False
    else:
        return True


def collect_album_items(bot, update, job_queue):
    """
    if the media_group_id not a key in the dictionary yet:
        - send sending action
        - create a key in the dict with media_group_id
        - add a list to the key and the first element is this message
        - schedule a job in 1 sec
    else:
        - add the message to the list of that media_group_id
    """
    media_group_id = update.message.media_group_id
    to_collect = {}
    to_collect['message_id'] = update.message.message_id
    to_collect['file_id'] = update.message.photo[-1].file_id if update.message.photo else update.message.video.file_id
    to_collect['caption'] = '' if update.message.caption is None else update.message.caption_html
    to_collect['type'] = 'photo' if update.message.photo else 'video'
    if media_group_id not in ALBUM_DICT:
        bot.sendChatAction(
            chat_id=update.message.from_user.id, 
            action=ChatAction.UPLOAD_PHOTO if update.message.photo else ChatAction.UPLOAD_VIDEO
        )
        ALBUM_DICT[media_group_id] = []
        ALBUM_DICT[media_group_id].append(to_collect)
        # schedule the job
        job_queue.run_once(send_album, 1, context=[update.message.from_user.id, media_group_id])
    else:
        ALBUM_DICT[media_group_id].append(to_collect)


def send_album(bot, job):
    user_id, media_group_id = job.context
    items = ALBUM_DICT[media_group_id]
    # delete from ALBUM_DICT
    del ALBUM_DICT[media_group_id]
    media = []
    for item in items:
        if item['type'] == 'photo':
            media.append(
                InputMediaPhoto(
                    media=item['file_id'],
                    caption=item['caption'],
                    parse_mode=ParseMode.HTML
                )
            )
        elif item['type'] == 'video':
            media.append(
                InputMediaVideo(
                    media=item['file_id'],
                    caption=item['caption'],
                    parse_mode=ParseMode.HTML
                )
            )
    bot.sendMediaGroup(
        chat_id=user_id,
        media=media
    )
