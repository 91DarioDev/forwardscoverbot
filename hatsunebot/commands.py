#!/usr/bin/env python

from hatsunebot import utils
from hatsunebot import keyboards
from hatsunebot import messages
from hatsunebot import config

#from telegram import MessageEntity
from telegram import ParseMode
#from telegram import constants as t_consts

from telegram.ext.dispatcher import run_async


@run_async
def help_command(bot, update):
    keyboard = keyboards.github_link_kb()
    text = (
        "<b>Do you want to send a ads message to someone or in a group, but you are not online forever</b>."
        "\n\nSend here what you want and set the time interval"
        "\n<i>It works also if you edit messages or forward messages. "
        "It also keeps the same text formatting style.</i>\n\n"
        "<b>Supported commands:</b>\n"
        "/set_send_target\n"
    )
    update.message.reply_text(
        text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


# send here
@run_async
def callback_minute(bot, job):

    try:
        while True:
            file_id = config.PHOTO_FILE_IP.pop(0)
            bot.send_photo(chat_id=config.CHAT_ID, photo=file_id, caption=None)
    except IndexError:
        pass

    # try:
    #     mid = config.MESSAGE_ID_LIST[0]
    #     fid = config.FROM_CHAT_ID_LIST[0]
    # except IndexError:
    #     return
    # bot.send_message(chat_id=config.CHAT_ID, text=send_message)
    # for c in config.CHAT_ID:
    #     bot.forwardMessage(chat_id=c, from_chat_id=fid, message_id=mid)

    # del config.MESSAGE_ID_LIST[0]
    # del config.FROM_CHAT_ID_LIST[0]
