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


import logging

# files
from forwardscoverbot import config
from forwardscoverbot import commands
from forwardscoverbot import messages
from forwardscoverbot import utils
from forwardscoverbot import albums
from forwardscoverbot import custom_filters

from telegram.ext import (
        Updater,
        CommandHandler,
        MessageHandler,
        Filters)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    print("\nrunning...")
    # define the updater
    updater = Updater(token=config.BOT_TOKEN, use_context=True)
    
    # define the dispatcher
    dp = updater.dispatcher

    # define jobs
    j = updater.job_queue

    # messages
    dp.add_handler(MessageHandler(Filters.all, messages.before_processing), 0)
    # albums
    dp.add_handler(MessageHandler(custom_filters.album, albums.collect_album_items), 1)
    # messages
    dp.add_handler(MessageHandler(Filters.all, messages.process_message), 1)
    # commands
    dp.add_handler(CommandHandler(('start', 'help'), commands.help_command), 2)
    dp.add_handler(CommandHandler('stats', commands.stats), 2)
    dp.add_handler(CommandHandler('disablewebpagepreview', commands.disable_web_page_preview), 2)
    dp.add_handler(CommandHandler('removecaption', commands.remove_caption), 2)
    dp.add_handler(CommandHandler('removebuttons', commands.remove_buttons), 2)
    dp.add_handler(CommandHandler('addcaption', commands.add_caption), 2)
    dp.add_handler(MessageHandler(Filters.command, utils.invalid_command), 2)


    # handle errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
