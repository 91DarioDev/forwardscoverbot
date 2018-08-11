#!/usr/bin/env python3

import pymysql
import logging
import sys
import random

from datetime import datetime

from hatsunebot import config


def get_max_tables():

    db = connect_mysql()
    cursor = db.cursor()
    cursor.execute(
        "SELECT table_rows FROM information_schema.tables WHERE table_schema='%s'" % config.SQL_DATABASE)
    rows = cursor.fetchall()
    config.NU_RANDOM = len(rows)
    close_mysql(db)


def random_pick_from_mysql(db):

    get_max_tables()
    table_id = random.randint(0, config.NU_RANDOM)
    table_name = "{0}pic_{1}".format(config.SQL_FORMAT, table_id)
    # logging.info(">>>>>>>>>>>>>>>>>>>table_name: {}".format(table_name))
    cursor_0 = db.cursor()
    cursor_0.execute(
        "SELECT table_rows FROM information_schema.tables WHERE table_name='%s'" % table_name)

    rows = cursor_0.fetchone()[0]
    random_rows = random.randint(0, rows)
    # logging.info(">>>>>>>>>>>>>>>>>>>>>>random_rows: {}".format(random_rows))

    cursor_1 = db.cursor()
    cursor_1.execute("SELECT file_id FROM %s" % table_name)
    try:
        return_result = cursor_1.fetchall()[random_rows]
    except IndexError:
        return_result = random_pick_from_mysql(db)

    return return_result


def get_mysql_version(db):

    cursor = db.cursor()
    cursor.execute("SELECT version()")
    return cursor.fetchone()[0]


def check_same_value(db, file_id):

    get_max_tables()
    cursor = db.cursor()
    for i in range(0, config.NU_RANDOM):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        cursor.execute("SELECT * FROM %s WHERE file_id = '%s' limit 1" %
                       (table_name, file_id))
        try:
            rows = cursor.fetchone()[0]
            return 1
        except Exception:
            pass

    return 0


def create_new_tables(db, table_name):

    cursor = db.cursor()
    # not test yet
    try:
        if cursor.execute("CREATE TABLE %s (file_id CHAR(100) NOT NULL, date CHAR(10))" % table_name) == 1:
            return 0
        else:
            return 1
    except Exception:
        return 1


def connect_mysql():

    # now connect to msyql
    try:
        db = pymysql.connect(config.SQL_SERVER, config.SQL_USER,
                             config.SQL_PASSWORD, config.SQL_DATABASE)
        logging.debug("Connect to {}".format(get_mysql_version(db)))
        return db
    except Exception:
        logging.error("Can't connected to mysql server...")
        sys.exit(1)


def check_table_full(db, table_name):

    cursor = db.cursor()
    cursor.execute(
        "SELECT table_rows FROM information_schema.tables WHERE table_name='%s'" % table_name)
    rows = cursor.fetchall()
    logging.debug(">>>>>>>>>>>>>>>>>>>>>")
    logging.debug(rows)
    if len(rows) == 0:
        rows = 0
    else:
        rows = rows[0][0]

    if rows >= config.MAX_ROWS:
        return 1
    else:
        return 0


def insert_mysql(db, file_id, date):

    cursor = db.cursor()
    get_max_tables()
    all_full = True
    if check_same_value(db, file_id) == 1:
        return

    for i in range(0, config.NU_RANDOM):
        logging.debug(">>>>>>>>>>>>>>>>>>>>>>>>{}".format(i))
        # we check all the database is full or not
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        if check_table_full(db, table_name) == 1:
            continue
        else:
            all_full = False
            cursor.execute("INSERT INTO %s(file_id, date) VALUES ('%s', '%s')" % (
                table_name, file_id, date))
        # db.commit()
    if all_full == True:
        table_name = "{0}pic_{1}".format(
            config.SQL_FORMAT, config.NU_RANDOM + 1)
        create_new_tables(db, table_name)
        try:
            cursor.execute("INSERT INTO %s(file_id, date) VALUES ('%s', '%s')" % (
                table_name, file_id, date))
        except Exception:
            return 1
    return 0
    # db.rollback()


def commit_mysql(db):

    db.commit()


def rollback_mysql(db):

    db.rollback()


def close_mysql(db):

    logging.debug('Close mysql connection')
    db.close()


def process_sql(file_id):

    if config.SQL_STATUS == True:
        db = connect_mysql()
        dt = datetime.now()
        date = dt.strftime('%Y_%m_%d_%I_%M_%S')
        if insert_mysql(db, file_id, date) == 1:
            db.rollback()
        return db
    else:
        pass
