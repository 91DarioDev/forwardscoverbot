#!/usr/bin/env python3

import pymysql
import logging
import sys
import random

from datetime import datetime

from hatsunebot import config


def random_pick_from_mysql(db):

    db = connect_mysql()
    table_id = random.randint(0, config.NU)
    table_name = "{0}pic_{1}".format(config.SQL_FORMAT, table_id)
    logging.info(">>>>>>>>>>>>>>>>>>>table_name: {}".format(table_name))
    cursor_0 = db.cursor()
    cursor_0.execute(
        "SELECT table_rows FROM information_schema.tables WHERE table_name='%s'" % table_name)

    rows = cursor_0.fetchone()[0]
    random_rows = random.randint(0, rows)
    logging.info(">>>>>>>>>>>>>>>>>>>>>>random_rows: {}".format(random_rows))

    cursor_1 = db.cursor()
    cursor_1.execute("SELECT file_id FROM %s" % table_name)
    try:
        return_result = cursor_1.fetchall()[random_rows]
    except IndexError:
        return_result = random_pick_from_mysql()

    return return_result


def get_mysql_version(db):

    cursor = db.cursor()
    cursor.execute("SELECT version()")
    return cursor.fetchone()[0]


def check_same_value(db, file_id):

    cursor = db.cursor()
    for i in range(0, config.NU + 1):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        cursor.execute("SELECT * FROM %s WHERE file_id = '%s' limit 1" %
                       (table_name, file_id))
        try:
            rows = cursor.fetchone()[0]
            return 1
        except Exception:
            pass

    return 0


def check_mysql_full(db, table_name):

    cursor = db.cursor()
    # not test yet
    try:
        cursor.execute(
            "SELECT table_rows FROM information_schema.tables WHERE table_name='%s'" % table_name)
        rows = cursor.fetchone()[0]
        # logging.debug(">>>>>>>>>>>>>>>>>>>>>")
        # logging.debug(rows)
    except Exception:
        return -1
    try:
        if int(rows) >= config.MAX_ROWS:
            return 1
    except TypeError:
        return -1
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


def insert_mysql(db, table_name, file_id, date):

    cursor = db.cursor()
    if check_same_value(db, file_id) == 1:
        return
    try:
        cursor.execute("INSERT INTO %s(file_id, date) VALUES ('%s', '%s')" % (
            table_name, file_id, date))
        # db.commit()
        return 0
    except Exception:
        return 1
        # db.rollback()


def commit_mysql(db):

    db.commit()


def rollback_mysql(db):

    db.rollback()


def close_mysql(db):

    logging.debug('Close mysql connection')
    db.close()


def process_sql(file_id, table_name):

    if config.SQL_STATUS == True:
        db = connect_mysql()
        while True:
            check_result = check_mysql_full(db, table_name)
            if check_result == 1:
                config.NU += 1
                table_name = "{0}pic_{1}".format(config.SQL_FORMAT, config.NU)
                process_sql(file_id, table_name)
                # create_new_tables(db, table_name)
                # config.CURRENT_TABLE = table_name
                break

            elif check_result == -1:
                table_name = "{0}pic_{1}".format(config.SQL_FORMAT, config.NU)
                create_new_tables(db, table_name)
                config.CURRENT_TABLE = table_name
                break

            elif check_result == 0:
                config.CURRENT_TABLE = table_name
                break
            config.NU += 1

        dt = datetime.now()
        date = dt.strftime('%Y-%m-%d-%I:%M:%S-%p')
        if insert_mysql(db, config.CURRENT_TABLE, file_id, date) == 1:
            db.rollback()
        return db
    else:
        pass
