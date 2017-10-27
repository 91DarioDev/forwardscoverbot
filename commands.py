# ForwardsCoverBot - don't let people on telegram forward with your name on the forward label
# Copyright (C) 2017  Dario dariomsn@hotmail.it

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import utils
import database
import keyboards

from telegram import MessageEntity
from telegram import ParseMode


def help_command(bot, update):
    keyboard = keyboards.github_link_kb()
    text = "<b>Do you want to send a message to someone or in a group, but you want to avoid that someone could \
spread it on telegram with your name? This bot just echos your messages</b>.\n\nSend here what you \
want and you will get the same message back, then forward the message where you want \
and the forward label will have the name of this bot.\n<i>It works also if you edit messages or forward \
messages. It also keeps the same text formatting style.</i>"
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


def disable_web_page_preview(bot, update):
    if not update.message.reply_to_message:
        text = "This command permits to remove the web page preview from a message with a link.\n\n\
Use it replying to the message the bot already echoed and you want to disable the preview with this command."
        update.message.reply_text(text=text)
        return

    if not update.message.reply_to_message.text:
        text = "This message does not have a web page preview"
        update.message.reply_to_message.reply_text(text=text, quote=True)
        return

    entities = update.message.reply_to_message.parse_entities([MessageEntity.URL, MessageEntity.TEXT_LINK])
    if len(entities) == 0:
        text = "This message does not have a web page preview"
        update.message.reply_to_message.reply_text(text=text, quote=True)
        return

    text = update.message.reply_to_message.text_html
    update.message.reply_to_message.reply_text(text=text, disable_web_page_preview=True, parse_mode=ParseMode.HTML)


@utils.only_admin
def stats(bot, update):
    update.message.reply_text(text=database.stats_text(), parse_mode=ParseMode.HTML)


