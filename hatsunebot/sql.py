#!/usr/bin/env python3

import pymysql
import logging
import sys
import time

from hatsunebot import config


def get_mysql_version(db):

    cursor = db.cursor()
    cursor.execute("SELECT version()")
    return cursor.fetchone()


def check_mysql_full(db, database_name):

    cursor = db.cursor()
    # not test yet
    try:
        cursor.execute(
            "select table_rows from information_schema.tables where table_schema='{}'".format(database_name))
        rows = cursor.fetchone()
    except Exception:
        return -1
    if int(rows) >= config.MAX_ROWS:
        return 1
    return 0


def create_new_tables(db, table_name):

    cursor = db.cursor()
    # not test yet
    try:
        cursor.execute(
            "CREATE TABLE {0} (file_id CHAR(100) NOT NULL, date CHAR(10) NOT NULL".format(table_name))
        return 0
    except Exception:
        return 1


def connect_mysql():

    # now connect to msyql
    try:
        db = pymysql.connect(config.SQL_SERVER, config.SQL_USER,
                             config.SQL_PASSWORD, config.SQL_DATABASE)
        logging.info("Connect to {}".format(get_mysql_version))
        return db
    except Exception:
        logging.error("Can't connected to mysql server...")
        sys.exit(1)


def insert_mysql(db, table_name, file_id, date):

    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO {0}(file_id, date) VALUES ({1}, {2})".format(table_name, file_id, date))
        db.commit()
    except Exception:
        db.rollback()


def process_sql(file_id):

    if config.SQL_STATUS == True:
        db = connect_mysql()
        nu = 0
        while True:
            table_name = "{0}pic_{1}".format(config.SQL_FORMAT, nu)
            check_result = check_mysql_full(db, table_name)
            if check_result == -1:
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
        insert_mysql(db, config.CURRENT_TABLE, file_id, date)
        db.close()
    else:
        pass
