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


from functools import wraps
from forwardscoverbot import config

from telegram.ext.dispatcher import run_async


def sep(num, none_is_zero=False):
    if num is None:
        return 0 if none_is_zero is True else None
    return "{:,}".format(num)


@run_async
def invalid_command(update, context):
    text = "This command is invalid"
    update.message.reply_text(text=text, quote=True)


def only_admin(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if update.message.from_user.id not in config.ADMINS:
            invalid_command(update, context, *args, **kwargs)
            return
        return func(update, context, *args, **kwargs)
    return wrapped

