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

import sqlite3
import time
import threading

from forwardscoverbot import utils
from forwardscoverbot import config

from telegram.ext.dispatcher import run_async


LOCAL = threading.local()

def conn():
    if not hasattr(LOCAL, "db"):
        LOCAL.db = sqlite3.connect(config.DB_PATH)
    return LOCAL.db


def run_query(query, *params, read=False, one=False):
    connect = conn()
    cursor = connect.cursor()
    try:
        cursor.execute(query, params)
        cursor.connection.commit()
        if read:
            if not one:
                return cursor.fetchall()
            else:
                return cursor.fetchone()
    except:
        cursor.connection.rollback()
        raise
    finally:
        cursor.close()


def create_db():
    query = "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, last_activity INTEGER)"
    run_query(query)


@run_async
def add_user_db(user_id, int_time):
    # try to update or ignore
    query = "UPDATE OR IGNORE users SET last_activity = ? WHERE user_id = ?"
    run_query(query, int_time, user_id)
    # try to add or ignore
    query = "INSERT OR IGNORE INTO users(user_id, last_activity) VALUES (?, ?)"
    run_query(query, user_id, int_time)


def stats_text():
    query = "SELECT count(user_id) FROM users"
    total = run_query(query, read=True, one=True)[0]

    interval24h = time.time() - 60*60*24
    query = "SELECT count(user_id) FROM users WHERE last_activity > ?"
    last24h = run_query(query, interval24h, read=True, one=True)[0]

    interval7d = time.time() - 60*60*24*7
    query = "SELECT count(user_id) FROM users WHERE last_activity > ?"
    last7d = run_query(query, interval7d, read=True, one=True)[0]

    text = "<b>Total users:</b> {0}\n<b>Last7days:</b> {1}\n<b>Last24h:</b> {2}"
    text = text.format(utils.sep(total), utils.sep(last7d), utils.sep(last24h))
    return text


# create the database
create_db()

