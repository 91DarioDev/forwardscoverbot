#!/usr/bin/env python3

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
        commands.callback_minute_send, interval=24, first=0)
    # sql jobs
    job.run_repeating(
        commands.callback_sql, interval=6, first=0)
    # albums
    # many picture here
    dp.add_handler(MessageHandler(custom_filters.album,
                                  albums.collect_album_items, pass_job_queue=True), 1)
    # messages
    dp.add_handler(MessageHandler(
        Filters.all, messages.process_message, edited_updates=True), 1)
    # commands
    dp.add_handler(CommandHandler('show', commands.help_command), 2)
    # turn series
    # dp.add_handler(CommandHandler(
    #     'turn_off_mysql', commands.turn_off_sql), 2)
    # dp.add_handler(CommandHandler('turn_on_mysql', commands.turn_on_sql), 2)
    # stop series
    dp.add_handler(CommandHandler('stop_forward', commands.stop_forward), 2)
    dp.add_handler(CommandHandler('start_forward', commands.start_forward), 2)
    # check existed in MySQL or not
    dp.add_handler(CommandHandler('check_existed', commands.check_existed), 2)
    # delete the same value in MySQL
    dp.add_handler(CommandHandler('delete_same', commands.delete_same), 2)
    # show check result
    dp.add_handler(CommandHandler('check_result_show',
                                  commands.check_result_show), 2)
    # random
    dp.add_handler(CommandHandler('random', commands.random_pic), 2)
    dp.add_handler(CommandHandler('help', commands.common_help_show), 2)
    # invalid_command
    dp.add_handler(MessageHandler(Filters.command, utils.invalid_command), 2)

    # handle errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
