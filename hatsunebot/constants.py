#!/usr/bin/env python

import sys

from hatsunebot import config

from telegram import Bot
from telegram import TelegramError

try:
    GET_ME = Bot(config.BOT_TOKEN).getMe(timeout=30)
except TelegramError:
    print("Bot auth failed.")
    sys.exit()
