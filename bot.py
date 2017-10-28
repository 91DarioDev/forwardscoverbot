# ForwardsCoverBot - don't let people on telegram forward with your name on the forward label
# Copyright (C) 2017  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)

# ForwardsCoverBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ForwardsCoverBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ForwardsCoverBot.  If not, see <http://www.gnu.org/licenses/>.


import logging

# files
from forwardscoverbot import config
from forwardscoverbot import commands
from forwardscoverbot import messages
from forwardscoverbot import utils

from telegram.ext import (
        Updater,
        CommandHandler,
        MessageHandler,
        Filters)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # define the updater
    updater = Updater(token=config.BOT_TOKEN)
    
    # define the dispatcher
    dp = updater.dispatcher

    # messages
    dp.add_handler(MessageHandler(Filters.all, messages.before_processing), 0)
    # messages
    dp.add_handler(MessageHandler(Filters.all, messages.process_message, edited_updates=True), 1)
    # commands
    dp.add_handler(CommandHandler(('start', 'help'), commands.help_command), 2)
    dp.add_handler(CommandHandler('stats', commands.stats), 2)
    dp.add_handler(CommandHandler('disablewebpagepreview', commands.disable_web_page_preview), 2)
    dp.add_handler(MessageHandler(Filters.command, utils.invalid_command), 2)


    # handle errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
