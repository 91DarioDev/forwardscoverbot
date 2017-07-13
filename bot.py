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



from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler  
import logging

#files
from config import configfile
import database
import commands
import messages


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
	logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
	#  define the updater
	updater = Updater(token=configfile.bot_token)
	
	# define the dispatcher
	dp = updater.dispatcher

	# messages
	dp.add_handler(MessageHandler(Filters.all, messages.before_processing), -1)
	# commands
	dp.add_handler(CommandHandler(('start', 'help'), commands.help_command))
	dp.add_handler(CommandHandler('stats', commands.stats))
	dp.add_handler(CommandHandler('disablewebpagepreview', commands.disable_web_page_preview))
	dp.add_handler(MessageHandler(Filters.command, commands.invalid_command))
	# messages
	dp.add_handler(MessageHandler(~Filters.command, messages.process_message, edited_updates=True))

	# handle errors
	dp.add_error_handler(error)


	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()