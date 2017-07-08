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


from telegram import ParseMode
import utils
import database


def help_command(bot, update):
	text = "<b>Do you want to send a message to someone or in a group, but you want to avoid that someone could \
spread it on telegram with your name? This bot just echos your messages</b>.\n\nSend here what you \
want and you will get the same message back, then forward the message where you want \
and the forward label will have the name of this bot.\n<i>It works also if you edit messages or forward \
messages. It also keeps the same text formatting style.</i>\
\n<a href=\"https://github.com/91DarioDev/ForwardsCoverBot\">Source code of the bot</a>"
	update.message.reply_text(text=text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

def invalid_command(bot, update):
	text = "This command is invalid"
	update.message.reply_text(text=text, quote=True)

def stats(bot, update):
	if utils.not_allowed(bot, update):
		invalid_command(bot, update)
		return
	update.message.reply_text(text=database.stats_text(), parse_mode=ParseMode.HTML)