#!/usr/bin/env python3


from telegram import ParseMode
from telegram.ext import DispatcherHandlerStop
from telegram.ext.dispatcher import run_async

from hatsunebot import keyboards
from hatsunebot import config
from hatsunebot.utils import only_admin
from hatsunebot.utils import full_list
from hatsunebot.utils import delete_command
from hatsunebot import error_log
from hatsunebot import sql


@run_async
def process_message_subdivision(bot, update, message, caption):

    # then use the message
    if message.text:
        # here we add the reply same words
        message.reply_text(text=message.text_html, parse_mode=ParseMode.HTML)
        pass

    elif message.voice:
        # media = message.voice.file_id
        # duration = message.voice.duration
        # message.reply_voice(voice=media, duration=duration, caption=caption, parse_mode=ParseMode.HTML)
        pass

    # here we work
    elif message.photo:
        # This is what the bot do now
        # we will send all the message
        # media = message.photo[-1].file_id
        # from_chat_id = message.chat.id
        # config.FROM_CHAT_ID_LIST.append(from_chat_id)

        # message_id = message.message_id
        # config.MESSAGE_ID_LIST.append(message_id)
        # message.reply_photo(photo=media, caption=caption, parse_mode=ParseMode.HTML)
        pass

    elif message.sticker:
        # media = message.sticker.file_id
        # message.reply_sticker(sticker=media)
        pass

    elif message.document:
        # media = message.document.file_id
        # filename = message.document.file_name
        # message.reply_document(document=media, filename=filename, caption=caption, parse_mode=ParseMode.HTML)
        pass

    elif message.audio:
        # media = message.audio.file_id
        # duration = message.audio.duration
        # performer = message.audio.performer
        # title = message.audio.title
        # message.reply_audio(audio=media, duration=duration, performer=performer, title=title, caption=caption, parse_mode=ParseMode.HTML)
        pass

    elif message.video:
        # media = message.video.file_id
        # duration = message.video.duration
        # message.reply_video(video=media, duration=duration, caption=caption, parse_mode=ParseMode.HTML)
        pass

    elif message.contact:
        # phone_number = message.contact.phone_number
        # first_name = message.contact.first_name
        # last_name = message.contact.last_name
        # message.reply_contact(phone_number=phone_number, first_name=first_name, last_name=last_name)
        pass

    elif message.venue:
        # longitude = message.venue.location.longitude
        # latitude = message.venue.location.latitude
        # title = message.venue.title
        # address = message.venue.address
        # foursquare_id = message.venue.foursquare_id
        # message.reply_venue(longitude=longitude, latitude=latitude, title=title, address=address, foursquare_id=foursquare_id)
        pass

    elif message.location:
        # longitude = message.location.longitude
        # latitude = message.location.latitude
        # message.reply_location(latitude=latitude, longitude=longitude)
        pass

    elif message.video_note:
        # media = message.video_note.file_id
        # length = message.video_note.length
        # duration = message.video_note.duration
        # message.reply_video_note(video_note=media, length=length, duration=duration)
        pass

    elif message.game:
        # text = "Sorry, telegram doesn't allow to echo this message"
        # message.reply_text(text=text, quote=True)
        pass

    else:
        # text = "Sorry, this kind of media is not supported yet"
        # text = "Thanks"
        # message.reply_text(text=text, quote=True)
        pass


@run_async
@only_admin
def process_message(bot, update, remove_caption=False, custom_caption=None):

    if update.message.forward_from_chat:
        if update.message.forward_from_chat.username not in config.ADMINS_GROUP:
            # print(update.message.forward_from_chat.username)
            # print(config.ADMINS_GROUP)
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
        # caption is message title
        caption = message.caption_html if (
            message.caption and remove_caption is False) else None
    else:
        caption = custom_caption

    if message.photo:

        # FIVE_TYPE_LIST = [[MESSAGE_ID, FROM_CHAT_ID， FILE_ID_1, FILE_ID_2, FILE_ID_3], [MESSAGE_ID, FROM_CHAT_ID, FILE_ID, FILE_ID_2, FILE_ID_3]]
        tmp_list = []
        message_id = message.message_id
        tmp_list.append(message_id)
        # config.MESSAGE_ID_LIST.append(message_id)
        from_chat_id = message.chat.id
        tmp_list.append(from_chat_id)
        # config.FROM_CHAT_ID_LIST.append(from_chat_id)

        # now we get them all
        for f in message.photo:
            file_id = f.file_id
            tmp_list.append(file_id)
            # config.PHOTO_FILE_ID.append(file_id)

        try:
            tmp_list = full_list(tmp_list)
        except Exception as e:
            e = 'process_message() tmp_list failed: ' + str(e.args)
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

            '''
            text = 'message_id:\n{0}:{1}\nfile_id_1:\n{2}:{3}\nfile_id_2:\n{4}:{5}\nfile_id_3:\n{6}:{7}\n'.format(
                mid, result_list[0], file_id_1, result_list[1], file_id_2, result_list[2], file_id_3, result_list[3])
            text = 'message_id:\n{0}\nfile_id_1:\n{1}\nfile_id_2:\n{2}\nfile_id_3:\n{3}\n'.format(
                result_list[0], result_list[1], result_list[2], result_list[3])
            '''
            # text = 'file_id_1:\n{0}\nfile_id_2:\n{1}\nfile_id_3:\n{2}\n'.format(
            #     result_list[0], result_list[1], result_list[2])
            # update.message.reply_text(text=text, quote=True)

            if config.CHECK_SHOW == True:

                # more information
                text = 'Extra show:\nfile_id_1:\n{0}\nfile_id_2:\n{1}\nfile_id_3:\n{2}\n'.format(
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

    process_message_subdivision(bot, update, message, caption)
