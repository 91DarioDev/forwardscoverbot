#!/usr/bin/env python

# python lib
import logging

# files
from hatsunebot import config
from hatsunebot import commands
from hatsunebot import messages
from hatsunebot import utils
from hatsunebot import albums
from hatsunebot import custom_filters

# use the python-telegram-bot lib
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler


# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                    level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    print("running...")
    # define the updater
    updater = Updater(token=config.BOT_TOKEN)

    # define the dispatcher
    dp = updater.dispatcher

    # define jobs
    job = updater.job_queue
    job.run_repeating(
        commands.callback_minute, interval=60, first=0)

    # albums
    dp.add_handler(MessageHandler(custom_filters.album,
                                  albums.collect_album_items, pass_job_queue=True), 1)
    # messages
    dp.add_handler(MessageHandler(
        Filters.all, messages.process_message, edited_updates=True), 1)
    # commands
    dp.add_handler(CommandHandler(('start', 'help'), commands.help_command), 2)
    # dp.add_handler(CommandHandler('set_ads_time', commands.set_ads_time), 2)
    # dp.add_handler(CommandHandler('disablewebpagepreview', commands.disable_web_page_preview), 2)
    # dp.add_handler(CommandHandler('removecaption', commands.remove_caption), 2)
    # dp.add_handler(CommandHandler('addcaption', commands.add_caption), 2)
    dp.add_handler(MessageHandler(Filters.command, utils.invalid_command), 2)

    # handle errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
