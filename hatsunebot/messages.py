#!/usr/bin/env python

from telegram import ParseMode
from telegram.ext import DispatcherHandlerStop

from hatsunebot import keyboards
from hatsunebot import config
from hatsunebot import utils

from telegram.ext.dispatcher import run_async


@run_async
def process_message(bot, update, remove_caption=False, custom_caption=None):

    if update.message.from_user.id not in config.ADMINS:
        utils.invalid_command(bot, update)
        return
    # here get the message
    if update.edited_message:
        message = update.edited_message
    elif remove_caption:
        message = update.message.reply_to_message
    elif custom_caption is not None:
        message = update.message.reply_to_message
    else:
        message = update.message

    if custom_caption is None:
        caption = message.caption_html if (
            message.caption and remove_caption is False) else None
    else:
        caption = custom_caption

    # then use the message
    if message.text:
        message.reply_text(text=message.text_html, parse_mode=ParseMode.HTML)

    elif message.voice:
        media = message.voice.file_id
        duration = message.voice.duration
        message.reply_voice(voice=media, duration=duration,
                            caption=caption, parse_mode=ParseMode.HTML)

    # here we work
    elif message.photo:
        # we will send all the message
        # media = message.photo[-1].file_id
        from_chat_id = message.chat.id
        config.FROM_CHAT_ID_LIST.append(from_chat_id)

        message_id = message.message_id
        config.MESSAGE_ID_LIST.append(message_id)
        # message.reply_photo(photo=media, caption=caption, parse_mode=ParseMode.HTML)

    elif message.sticker:
        media = message.sticker.file_id
        message.reply_sticker(sticker=media)

    elif message.document:
        media = message.document.file_id
        filename = message.document.file_name
        message.reply_document(
            document=media, filename=filename, caption=caption, parse_mode=ParseMode.HTML)

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
            parse_mode=ParseMode.HTML)

    elif message.video:
        media = message.video.file_id
        duration = message.video.duration
        message.reply_video(video=media, duration=duration,
                            caption=caption, parse_mode=ParseMode.HTML)

    elif message.contact:
        phone_number = message.contact.phone_number
        first_name = message.contact.first_name
        last_name = message.contact.last_name
        message.reply_contact(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name)

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
            foursquare_id=foursquare_id)

    elif message.location:
        longitude = message.location.longitude
        latitude = message.location.latitude
        message.reply_location(latitude=latitude, longitude=longitude)

    elif message.video_note:
        media = message.video_note.file_id
        length = message.video_note.length
        duration = message.video_note.duration
        message.reply_video_note(
            video_note=media, length=length, duration=duration)

    elif message.game:
        text = "Sorry, telegram doesn't allow to echo this message"
        message.reply_text(text=text, quote=True)

    else:
        # text = "Sorry, this kind of media is not supported yet"
        # text = "Thanks"
        # message.reply_text(text=text, quote=True)
        pass