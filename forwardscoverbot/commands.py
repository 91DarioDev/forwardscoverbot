# ForwardsCoverBot - don't let people on telegram forward with your name on the forward label
# Copyright (C) 2017-2020  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
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


from forwardscoverbot import utils
from forwardscoverbot import dbwrapper
from forwardscoverbot import keyboards
from forwardscoverbot import messages

from telegram import MessageEntity
from telegram import ParseMode
from telegram import constants as t_consts
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.ext.dispatcher import run_async

import html


def help_command(update, context):
    keyboard = keyboards.github_link_kb()
    text = (
        "<b>Do you want to send a message to someone or in a group, but you want to avoid "
        "that someone could spread it on telegram with your name? This bot just echos "
        "your messages</b>.\n\nSend here what you want and you will get the same message "
        "back, then forward the message where you want and the forward label will have "
        "the name of this bot.\n<i>It works also if you edit messages or forward messages. "
        "It also keeps the same text formatting style.</i>\n\n"
        "<b>Supported commands:</b>\n"
        "/disablewebpagepreview\n"
        "/removecaption\n"
        "/addcaption\n"
        "/removebuttons\n"
        "/addbuttons"
    )
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)



def disable_web_page_preview(update, context):
    if not update.message.reply_to_message:
        text = ("This command permits to remove the web page preview from a message with "
                "a link.\n\nUse it replying to the message the bot already echoed and you "
                "want to disable the preview with this command.")
        update.message.reply_text(text=text)
        return

    if not update.message.reply_to_message.text:
        text = "This message does not have a web page preview"
        update.message.reply_to_message.reply_text(text=text, quote=True)
        return

    entities_list = [MessageEntity.URL, MessageEntity.TEXT_LINK]
    entities = update.message.reply_to_message.parse_entities(entities_list)
    if len(entities) == 0:
        text = "This message does not have a web page preview"
        update.message.reply_to_message.reply_text(text=text, quote=True)
        return

    messages.process_message(update=update, context=context, message=update.message.reply_to_message, disable_web_page_preview=True)



def remove_caption(update, context):
    if not update.message.reply_to_message:
        text = (
            "This command permits to remove caption from a message. Reply with this command to "
            "the message where you want to remove the caption. Be sure the message has a caption."
        )
        update.message.reply_text(text=text)
        return

    if not update.message.reply_to_message.caption:
        text = "This message has no caption, so what should i remove? Use this command with messages having caption."
        context.bot.sendMessage(
            chat_id=update.message.from_user.id,
            text=text,
            reply_to_message_id=update.message.reply_to_message.message_id,
            quote=True
        )
        return

    messages.process_message(update=update, context=context, message=update.message.reply_to_message, remove_caption=True)



def remove_buttons(update, context):
    if not update.message.reply_to_message:
        text = (
            "This command permits to remove buttons from a message. Reply with this command to "
            "the message where you want to remove the buttons. Be sure the message has buttons."
        )
        update.message.reply_text(text=text)
        return

    if not update.message.reply_to_message.reply_markup:
        text = "This message has no buttons, so what should i remove? Use this command with messages having buttons."
        context.bot.sendMessage(
            chat_id=update.message.from_user.id,
            text=text,
            reply_to_message_id=update.message.reply_to_message.message_id,
            quote=True
        )
        return

    messages.process_message(update=update, context=context, message=update.message.reply_to_message, remove_buttons=True)    



def add_caption(update, context):
    if not update.message.reply_to_message:
        text = (
            "<b>This command permits to add a caption to a message. Reply with this command and the caption after it to "
            "the message where you want to add the caption.</b>\n\n<i>If the message already has a caption "
            "this command will overwrite the current caption with the new one.\n"
            "if the message doesn't support a caption, it simply won't add it, no errors are returned</i>\n\n\n"
            "<i>Note: if the message is sent by you, you can just edit it to add the caption. This command is intended "
            "in case for example you are fowarding from a channel a big file you don't want to download and "
            "upload again.</i>"
        )
        update.message.reply_text(text=text, parse_mode='HTML')
        return

    caption = " ".join(update.message.text.split(" ")[1:])
    caption_html = " ".join(update.message.text_html.split(" ")[1:])

    if len(caption) > t_consts.MAX_CAPTION_LENGTH:
        text = "This caption is too long. max allowed: {} chars. Please retry removing {} chars.".format(
            t_consts.MAX_CAPTION_LENGTH,
            len(caption) - t_consts.MAX_CAPTION_LENGTH
        )
        context.bot.sendMessage(
            chat_id=update.message.from_user.id,
            text=text,
            reply_to_message_id=update.message.reply_to_message.message_id,
            quote=True
        )
        return

    messages.process_message(update=update, context=context, message=update.message.reply_to_message, custom_caption=caption_html)



def add_buttons(update, context):
    usage = (
        "<b>Using this command you can add buttons to messages.</b>\nReply with this command to the message where you want to add the buttons. Example:\n\n"
        "<code>/addbuttons first link=https://telegram.org && second link same row=https://google.it &&& third link new row=https://t.me</code>"
        "\n\nSo the format for a button is [text]=[link]. Buttons on the same line are separated by && and on new lines are separeted by &&&."
    )
    if not update.message.reply_to_message or len(context.args) < 1:
        update.message.reply_text(text=usage, parse_mode='HTML')
        return
    
    param = ' '.join(context.args)
    rows = param.split('&&&')
    lst = []
    for row in rows:
        try:
            row_lst = []
            row_buttons = row.split('&&')
            for button in row_buttons:
                text, link = button.split('=')
                text = text.strip()
                link = link.strip()
                button = InlineKeyboardButton(text=text, url=link)
                
                row_lst.append(button)
            lst.append(row_lst)
        except Exception as e:
            error = 'ERROR formatting the buttons'
            update.message.reply_text(text=error, parse_mode='HTML')
    keyboard = InlineKeyboardMarkup(lst)
    messages.process_message(update=update, context=context, message=update.message.reply_to_message, custom_reply_markup=keyboard)
    

@utils.only_admin
def stats(update, context):
    update.message.reply_text(text=dbwrapper.stats_text(), parse_mode=ParseMode.HTML)



