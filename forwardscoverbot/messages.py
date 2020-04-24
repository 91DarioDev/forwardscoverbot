# ForwardsCoverBot - don't let people on telegram forward with your name on the forward label
# Copyright (C) 2017-2019  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
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


import time

from telegram import ParseMode
from telegram.ext import DispatcherHandlerStop
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from forwardscoverbot import dbwrapper
from forwardscoverbot import keyboards

from telegram.ext.dispatcher import run_async


def before_processing(update, context):
    if update.effective_chat.type != "private":
        text = "This bot can be used only in private chats! I leave! Bye!"
        keyboard = keyboards.private_chat_kb()
        update.effective_message.reply_text(text=text, reply_markup=keyboard)
        context.bot.leave_chat(chat_id=update.effective_message.chat_id)
        raise DispatcherHandlerStop
        
    else:
        int_time = int(time.mktime(update.effective_message.date.timetuple()))
        dbwrapper.add_user_db(update.effective_message.from_user.id, int_time)


def get_message_reply_markup_inline_keyboard(message):
    if not message.reply_markup:
        return None
    if not message.reply_markup.inline_keyboard:
        return None
    return message.reply_markup.inline_keyboard


def leave_only_url_buttons_in_reply_markup(inline_keyboard):
    removed_buttons = []
    for row in inline_keyboard:
        for button in row:
            if not hasattr(button, 'url'):
                row.remove(button)
                removed_buttons.append(button)
    return inline_keyboard, removed_buttons


@run_async
def process_message(update, context, remove_caption=False, custom_caption=None, remove_buttons=False):
    if update.edited_message:
        message = update.edited_message
    elif remove_caption:
        message = update.message.reply_to_message
    elif custom_caption is not None:
        message = update.message.reply_to_message
    elif remove_buttons:
        message = update.message.reply_to_message
    else:
        message = update.message

    if custom_caption is None:
        caption = message.caption_html if (message.caption and remove_caption is False) else None
    else:
        caption = custom_caption


    keyboard_not_cleaned = get_message_reply_markup_inline_keyboard(message) if not remove_buttons else None
    if keyboard_not_cleaned:
        inline_keyboard, removed_buttons_from_keyboard = leave_only_url_buttons_in_reply_markup(keyboard_not_cleaned)
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        if len(removed_buttons_from_keyboard) > 0:
            message.reply_text(
                '{} buttons have been removed. I support only link buttons'.format(
                    len(removed_buttons_from_keyboard)
                )
            )
    else:
        reply_markup = None


    if message.text:
        message.reply_text(
            text=message.text_html, 
            parse_mode=ParseMode.HTML, 
            reply_markup=reply_markup
        )

    elif message.voice:
        media = message.voice.file_id
        duration = message.voice.duration
        message.reply_voice(
            voice=media, 
            duration=duration, 
            caption=caption, 
            parse_mode=ParseMode.HTML, 
            reply_markup=reply_markup
        )

    elif message.photo:
        media = message.photo[-1].file_id
        message.reply_photo(
            photo=media, 
            caption=caption, 
            parse_mode=ParseMode.HTML, 
            reply_markup=reply_markup
        )

    elif message.sticker:
        media = message.sticker.file_id
        message.reply_sticker(
            sticker=media, 
            reply_markup=reply_markup
        )

    elif message.document:
        media = message.document.file_id
        filename = message.document.file_name
        message.reply_document(
            document=media, 
            filename=filename, 
            caption=caption, 
            parse_mode=ParseMode.HTML, 
            reply_markup=reply_markup
        )

    elif message.audio:
        media = message.audio.file_id
        duration = message.audio.duration
        performer = message.audio.performer
        title = message.audio.title
        message.reply_audio(
            audio=media, 
            duration=duration, 
            performer=performer, 
            title=title, 
            caption=caption, 
            parse_mode=ParseMode.HTML, 
            reply_markup=reply_markup
        )
    
    elif message.video:
        media = message.video.file_id
        duration = message.video.duration
        message.reply_video(
            video=media, 
            duration=duration, 
            caption=caption, 
            parse_mode=ParseMode.HTML, 
            reply_markup=reply_markup
        )

    elif message.contact:
        phone_number = message.contact.phone_number
        first_name = message.contact.first_name
        last_name = message.contact.last_name
        message.reply_contact(
            phone_number=phone_number, 
            first_name=first_name, 
            last_name=last_name, 
            reply_markup=reply_markup
        )

    elif message.venue:
        longitude = message.venue.location.longitude
        latitude = message.venue.location.latitude
        title = message.venue.title
        address = message.venue.address
        foursquare_id = message.venue.foursquare_id
        message.reply_venue(
            longitude=longitude, 
            latitude=latitude, 
            title=title, 
            address=address, 
            foursquare_id=foursquare_id, 
            reply_markup=reply_markup
        )

    elif message.location:
        longitude = message.location.longitude
        latitude = message.location.latitude
        message.reply_location(latitude=latitude, longitude=longitude, reply_markup=reply_markup)

    elif message.video_note:
        media = message.video_note.file_id
        length = message.video_note.length
        duration = message.video_note.duration
        message.reply_video_note(video_note=media, length=length, duration=duration, reply_markup=reply_markup)
    
    elif message.dice:
        context.bot.sendDice(chat_id=update.effective_user.id, reply_markup=reply_markup, emoji=message.dice.emoji)

    elif message.game:
        text = "Sorry, telegram doesn't allow to echo this message"
        message.reply_text(text=text, quote=True)

    else:
        text = "Sorry, this kind of media is not supported yet"
        message.reply_text(text=text, quote=True)
