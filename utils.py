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

from functools import wraps
from config import configfile


import locale
locale.setlocale(locale.LC_ALL,"")

def n_dots(number):
    number = locale.format("%d", number, grouping=True)
    return number


def invalid_command(bot, update):
    text = "This command is invalid"
    update.message.reply_text(text=text, quote=True)


def only_admin(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.message.from_user.id not in configfile.admins:
            invalid_command(bot, update, *args, **kwargs)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

