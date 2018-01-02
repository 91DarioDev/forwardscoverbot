# ForwardsCoverBot - don't let people on telegram forward with your name on the forward label
# Copyright (C) 2017-2018  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
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
    print("\nrunning...")
    # define the updater
    updater = Updater(token=config.BOT_TOKEN)
    
    # define the dispatcher
    dp = updater.dispatcher

    # define jobs
    j = updater.job_queue

    # messages
    dp.add_handler(MessageHandler(Filters.all, messages.before_processing), 0)
    # albums
    dp.add_handler(MessageHandler(Filters.photo | Filters.video, albums.possible_album_processing, pass_job_queue=True), 1)
    # messages
    dp.add_handler(MessageHandler(Filters.all, messages.process_message, edited_updates=True), 2)
    # commands
    dp.add_handler(CommandHandler(('start', 'help'), commands.help_command), 3)
    dp.add_handler(CommandHandler('stats', commands.stats), 3)
    dp.add_handler(CommandHandler('disablewebpagepreview', commands.disable_web_page_preview), 3)
    dp.add_handler(CommandHandler('removecaption', commands.remove_caption), 3)
    dp.add_handler(CommandHandler('addcaption', commands.add_caption), 3)
    dp.add_handler(MessageHandler(Filters.command, utils.invalid_command), 3)


    # handle errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
