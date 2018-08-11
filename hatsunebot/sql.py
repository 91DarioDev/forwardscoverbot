#!/usr/bin/env python3

import pymysql
import logging
import sys
import time

from hatsunebot import config


def get_mysql_version(db):

    cursor = db.cursor()
    cursor.execute("SELECT version()")
    return cursor.fetchone()[0]


def check_mysql_full(db, table_name):

    cursor = db.cursor()
    # not test yet
    try:
        cursor.execute("select table_rows from information_schema.tables where table_name='%s'" % table_name) == 1
        rows = cursor.fetchone()
        logging.info('>>>>>>>>>>>>>>>>>>>' + rows)
    except Exception:
        return -1
    if int(rows) >= config.MAX_ROWS:
        return 1
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
        logging.info("Connect to {}".format(get_mysql_version(db)))
        return db
    except Exception:
        logging.error("Can't connected to mysql server...")
        sys.exit(1)


def insert_mysql(db, table_name, file_id, date):

    cursor = db.cursor()
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

    logging.info('Close mysql connection')
    db.close()


def process_sql(file_id):

    if config.SQL_STATUS == True:
        db = connect_mysql()
        nu = 0
        while True:
            table_name = "{0}pic_{1}".format(config.SQL_FORMAT, nu)
            check_result = check_mysql_full(db, table_name)
            if check_result != 0:
                nu += 1
                table_name = "{0}pic_{1}".format(config.SQL_FORMAT, nu)
                create_new_tables(db, table_name)
                config.CURRENT_TABLE = table_name
                break

            elif check_result == 0:
                config.CURRENT_TABLE = table_name
                break
            nu += 1

        date = time.asctime(time.localtime(time.time()))
        if insert_mysql(db, config.CURRENT_TABLE, file_id, date) == 1:
            db.rollback()
        return db
    else:
        pass
