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
    # logging.debug(">>>>>>>>>>>>>>>>>>>table_name: {}".format(table_name))
    cursor_0 = db.cursor()
    cursor_0.execute(
        "SELECT table_rows FROM information_schema.tables WHERE table_name='%s'" % table_name)

    rows = cursor_0.fetchone()
    if rows is None:
        random_pick_from_mysql(db)
        return
    # print(rows)
    rows = rows[0]
    random_rows = random.randint(0, rows)
    # logging.debug(">>>>>>>>>>>>>>>>>>>>>>random_rows: {}".format(random_rows))

    cursor_1 = db.cursor()
    cursor_1.execute("SELECT message_id FROM %s" % table_name)

    try:
        r_mid = cursor_1.fetchall()
        # print(r_mid)
        r_mid = r_mid[random_rows][0]
    except IndexError:
        r_mid, r_fid = random_pick_from_mysql(db)

    cursor_2 = db.cursor()
    cursor_2.execute(
        "SELECT from_chat_id FROM %s WHERE message_id='%s'" % (table_name, r_mid))
    r_fid = cursor_2.fetchone()[0]

    return (r_mid, r_fid)


def get_mysql_version(db):

    cursor = db.cursor()
    cursor.execute("SELECT version()")
    return cursor.fetchone()[0]


def check_same_value(db, file_id):

    get_max_tables()
    cursor = db.cursor()
    for i in range(0, config.NU_RANDOM):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        cursor.execute("SELECT * FROM %s WHERE file_id_1='%s' limit 1" %
                       (table_name, file_id))
        if cursor.fetchone() != None:
            return 1

    return 0


def create_new_tables(db, table_name):

    cursor = db.cursor()
    # use the varchar for unsure date
    """
    [
        [3991, 366039180, 'AgADBQADHqgxG6docVevwzHBji_opA801TIABAqGbUg-S8HFP8ECAAEC'],
        [3991, 366039180, 'AgADBQADHqgxG6docVevwzHBji_opA801TIABFLydOubQv-6QMECAAEC'],
        [3991, 366039180, 'AgADBQADHqgxG6docVevwzHBji_opA801TIABPcr_ZfuycSkQcECAAEC'],
        [3991, 366039180, 'AgADBQADHqgxG6docVevwzHBji_opA801TIABAcJOOcyQWj8PsECAAEC'],
        [3992, 366039180, 'AgADBQADH6gxG6docVcHRcI6L68KiLRK1TIABIypPaslbU-akLICAAEC'],
        [3992, 366039180, 'AgADBQADH6gxG6docVcHRcI6L68KiLRK1TIABORRdKr0KXgRkbICAAEC'],
        [3992, 366039180, 'AgADBQADH6gxG6docVcHRcI6L68KiLRK1TIABAt95ny_A6KmkrICAAEC'],
        [3992, 366039180, 'AgADBQADH6gxG6docVcHRcI6L68KiLRK1TIABHhZdVsgP_YDj7ICAAEC'],
        [3993, 366039180, 'AgADBQADIKgxG6docVdP_5qOFLTLuk-p1jIABBgKpuOY0jmrxTkBAAEC'],
        [3993, 366039180, 'AgADBQADIKgxG6docVdP_5qOFLTLuk-p1jIABOQB-N1TfaNgxjkBAAEC'],
        [3993, 366039180, 'AgADBQADIKgxG6docVdP_5qOFLTLuk-p1jIABLYJfkdL-oupxDkBAAEC']
    ]
    """
    try:
        # message_id, from_chat_id， file_id_1, file_id_2, file_id_3
        if cursor.execute("CREATE TABLE %s (message_id CHAR(100) NOT NULL, from_chat_id CHAR(50) NOT NULL, file_id_1 VARCHAR(200), file_id_2 VARCHAR(200), file_id_3 VARCHAR(200), date VARCHAR(30))" % table_name) == 1:
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
        # logging.debug("Connect to {}".format(get_mysql_version(db)))
        return db
    except Exception:
        logging.error("Can't connected to mysql server...")
        sys.exit(1)


def check_table_full(db, table_name):

    cursor = db.cursor()
    cursor.execute(
        "SELECT table_rows FROM information_schema.tables WHERE table_name='%s'" % table_name)
    rows = cursor.fetchall()
    # logging.debug(">>>>>>>>>>>>>>>>>>>>>")
    # logging.debug(rows)
    if len(rows) == 0:
        rows = 0
    else:
        rows = rows[0][0]

    if rows >= config.MAX_ROWS:
        return 1
    else:
        return 0


def insert_mysql(db, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date):

    cursor = db.cursor()
    get_max_tables()
    all_full = True
    # Here we use the file_id_1 to check the same in mysql
    if check_same_value(db, file_id_1) == 1:
        return 0

    for i in range(0, config.NU_RANDOM):
        # logging.debug(">>>>>>>>>>>>>>>>>>>>>>>>{}".format(i))
        # we check all the database is full or not
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        if check_table_full(db, table_name) == 1:
            continue
        else:
            all_full = False
            # message_id, from_chat_id， file_id_1, file_id_2, file_id_3
            try:
                cursor.execute("INSERT INTO %s(message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                    table_name, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date))
            except Exception:
                return 1
    if all_full == True:
        table_name = "{0}pic_{1}".format(
            config.SQL_FORMAT, config.NU_RANDOM)
        create_new_tables(db, table_name)
        try:
            cursor.execute("INSERT INTO %s(message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                table_name, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date))
        except Exception:
            return 1
    return 0


def commit_mysql(db):

    db.commit()


def rollback_mysql(db):

    db.rollback()


def close_mysql(db):

    # logging.debug('Close mysql connection')
    db.close()


def process_sql(db, in_list):

    #            0              1           2          3           4
    # LIST = [MESSAGE_ID, FROM_CHAT_ID， FILE_ID_1, FILE_ID_2, FILE_ID_3]
    if config.SQL_STATUS == True:
        # db = connect_mysql()
        dt = datetime.now()
        date = dt.strftime('%Y-%m-%d %I:%M:%S')
        if insert_mysql(db, in_list[0], in_list[1], in_list[2], in_list[3], in_list[4], date) == 1:
            db.rollback()
    else:
        pass
