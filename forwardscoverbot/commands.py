# ForwardsCoverBot - don't let people on telegram forward with your name on the forward label
# Copyright (C) 2017-2022  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
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
from telegram.constants import ParseMode
from telegram.constants import MessageLimit
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


async def help_command(update, context):
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
        "/addbuttons\n"
        "/addspoiler\n"
        "/removespoiler\n"
    )
    await update.message.reply_text(text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)



async def disable_web_page_preview(update, context):
    if not update.message.reply_to_message:
        text = ("This command permits to remove the web page preview from a message with "
                "a link.\n\nUse it replying to the message the bot already echoed and you "
                "want to disable the preview with this command.")
        await update.message.reply_text(text=text)
        return

    if not update.message.reply_to_message.text:
        text = "This message does not have a web page preview"
        await update.message.reply_to_message.reply_text(text=text, quote=True)
        return

    entities_list = [MessageEntity.URL, MessageEntity.TEXT_LINK]
    entities = update.message.reply_to_message.parse_entities(entities_list)
    if len(entities) == 0:
        text = "This message does not have a web page preview"
        await update.message.reply_to_message.reply_text(text=text, quote=True)
        return

    await messages.process_message(update=update, context=context, message=update.message.reply_to_message, disable_web_page_preview=True)



async def remove_caption(update, context):
    if not update.message.reply_to_message:
        text = (
            "This command permits to remove caption from a message. Reply with this command to "
            "the message where you want to remove the caption. Be sure the message has a caption."
        )
        await update.message.reply_text(text=text)
        return

    if not update.message.reply_to_message.caption:
        text = "This message has no caption, so what should i remove? Use this command with messages having caption."
        await context.bot.sendMessage(
            chat_id=update.message.from_user.id,
            text=text,
            reply_to_message_id=update.message.reply_to_message.message_id
        )
        return

    await messages.process_message(update=update, context=context, message=update.message.reply_to_message, remove_caption=True)



async def add_spoiler(update, context):
    await handle_spoiler(update, context, 'add')


async def remove_spoiler(update, context):
    await handle_spoiler(update, context, 'remove')


async def handle_spoiler(update, context, spoiler_action):
    if not update.message.reply_to_message:
        if spoiler_action == 'add':
            text = (
                "This command permits to add a spoiler to a message. Reply with this command to "
                "the message where you want to add the spoiler."
            )
        elif spoiler_action == 'remove':
            text = (
                "This command permits to remove the spoiler from a message. Reply with this command to "
                "the message where you want to remove the spoiler."
            )
        await update.message.reply_text(text=text)
        return

    
    if not (update.message.reply_to_message.photo or update.message.reply_to_message.video or update.message.reply_to_message.animation):
        text = "This message doesn't support spoilers."
        await context.bot.sendMessage(
            chat_id=update.message.from_user.id,
            text=text,
            reply_to_message_id=update.message.reply_to_message.message_id,
        )
        return

    await messages.process_message(update=update, context=context, message=update.message.reply_to_message, spoiler_action=spoiler_action)


async def remove_buttons(update, context):
    if not update.message.reply_to_message:
        text = (
            "This command permits to remove buttons from a message. Reply with this command to "
            "the message where you want to remove the buttons. Be sure the message has buttons."
        )
        await update.message.reply_text(text=text)
        return

    if not update.message.reply_to_message.reply_markup:
        text = "This message has no buttons, so what should i remove? Use this command with messages having buttons."
        await context.bot.sendMessage(
            chat_id=update.message.from_user.id,
            text=text,
            reply_to_message_id=update.message.reply_to_message.message_id
        )
        return

    await messages.process_message(update=update, context=context, message=update.message.reply_to_message, remove_buttons=True)    



async def add_caption(update, context):
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
        await update.message.reply_text(text=text, parse_mode='HTML')
        return

    caption = " ".join(update.message.text.split(" ")[1:])
    caption_html = " ".join(update.message.text_html.split(" ")[1:])

    if len(caption) > MessageLimit.CAPTION_LENGTH:
        text = "This caption is too long. max allowed: {} chars. Please retry removing {} chars.".format(
            MessageLimit.CAPTION_LENGTH,
            len(caption) - MessageLimit.CAPTION_LENGTH 
        )
        await context.bot.sendMessage(
            chat_id=update.message.from_user.id,
            text=text,
            reply_to_message_id=update.message.reply_to_message.message_id
        )
        return

    await messages.process_message(update=update, context=context, message=update.message.reply_to_message, custom_caption=caption_html)



async def add_buttons(update, context):
    usage = (
        "<b>Using this command you can add buttons to messages.</b>\nReply with this command to the message where you want to add the buttons. Example:\n\n"
        "<code>/addbuttons first link=https://telegram.org && second link same row=https://google.it &&& third link new row=https://t.me</code>"
        "\n\nSo the format for a button is [text]=[link]. Buttons on the same line are separated by && and on new lines are separeted by &&&."
    )
    if not update.message.reply_to_message or len(context.args) < 1:
        await update.message.reply_text(text=usage, parse_mode='HTML')
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
            await update.message.reply_text(text=error, parse_mode='HTML')
    keyboard = InlineKeyboardMarkup(lst)
    await messages.process_message(update=update, context=context, message=update.message.reply_to_message, custom_reply_markup=keyboard)
    

@utils.only_admin
async def stats(update, context):
    await update.message.reply_text(text=await dbwrapper.stats_text(), parse_mode=ParseMode.HTML)



