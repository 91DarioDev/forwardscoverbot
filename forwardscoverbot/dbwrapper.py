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

import sqlite3
import time

from forwardscoverbot import utils
from config import configfile


def connect():
    conn = sqlite3.connect("database/"+configfile.DB_NAME)
    c = conn.cursor()
    return conn, c


def query_w(query, *params):
    conn, c = connect()
    c.execute(query, params)
    conn.commit()
    conn.close()


def query_r(query, *params, one=False):
    conn, c = connect()
    c.execute(query, params)
    try:
        if not one:
            return c.fetchall()
        else:
            return c.fetchone()
    finally:
        conn.close()


def create_db():
    query = "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, last_activity INTEGER)"
    query_w(query)


def add_user_db(user_id, int_time):
    # try to update or ignore
    query = "UPDATE OR IGNORE users SET last_activity = ? WHERE user_id = ?"
    query_w(query, int_time, user_id)
    # try to add or ignore
    query = "INSERT OR IGNORE INTO users(user_id, last_activity) VALUES (?, ?)"
    query_w(query, user_id, int_time)


def stats_text():
    query = "SELECT count(user_id) FROM users"
    total = query_r(query, one=True)[0]

    interval24h = time.time() - 60*60*24
    query = "SELECT count(user_id) FROM users WHERE last_activity > ?"
    last24h = query_r(query, interval24h, one=True)[0]

    interval7d = time.time() - 60*60*24*7
    query = "SELECT count(user_id) FROM users WHERE last_activity > ?"
    last7d = query_r(query, interval7d, one=True)[0]

    text = "<b>Total users:</b> {0}\n<b>Last7days:</b> {1}\n<b>Last24h:</b> {2}"
    text = text.format(utils.sep(total), utils.sep(last7d), utils.sep(last24h))
    return text


# create the database
create_db()

