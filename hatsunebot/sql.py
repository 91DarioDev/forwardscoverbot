#!/usr/bin/env python3

import pymysql
import logging
import sys
import random
from datetime import datetime

from hatsunebot import config
from hatsunebot import error_log


def get_max_tables():

    db = connect_mysql()
    cursor = db.cursor()
    # get how many tables we have in the database
    cursor.execute(
        "SELECT table_rows FROM information_schema.tables WHERE table_schema='%s'" % config.SQL_DATABASE)
    rows = cursor.fetchall()
    config.NU_RANDOM = len(rows)
    close_mysql(db)


def select_fid(db, table_name, mid):

    cursor = db.cursor()
    while True:
        cursor.execute(
            "SELECT from_chat_id FROM %s WHERE message_id='%s'" % (table_name, mid))
        fid = cursor.fetchone()[0]
        if fid != None:
            break

    # print(">>>>>>>>>>>>>>>>>>>>>>>>>{}".format(fid))
    return fid


def random_pick_mid(db, table_name):

    cursor_0 = db.cursor()
    cursor_1 = db.cursor()
    mid = -1
    while True:
        cursor_0.execute(
            "SELECT table_rows FROM information_schema.tables WHERE table_name='%s'" % table_name)

        rows = cursor_0.fetchone()[0]
        random_rows = random.randint(0, rows)

        cursor_1.execute("SELECT message_id FROM %s" % table_name)

        mid = cursor_1.fetchall()[random_rows][0]
        if mid:
            # print(mid)
            break

    # print(">>>>>>>>>>>>>>>>>>>>>>>>>{}".format(mid))

    if mid != -1:
        return (mid, random_rows)
    else:
        raise Exception('We can NOT get the mid')


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
        if len(cursor.fetchone()) != 0:
            # we have the same value in MySQL
            # so we return 1
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
    except Exception as e:
        e = 'create_new_tables() execute failed: ' + str(e.args)
        error_log.write_it(e)
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


def return_table_rows(db, table_name):

    cursor = db.cursor()
    cursor.execute(
        "SELECT table_rows FROM information_schema.tables WHERE table_name='%s' AND table_schema='%s'" % (table_name, config.SQL_DATABASE))

    rows = cursor.fetchone()
    # logging.debug(">>>>>>>>>>>>>>>>>>>>>")
    # logging.debug(rows)
    if len(rows) == 0:
        rows = 0
    else:
        rows = rows[0]

    return rows


def check_table_full(db, table_name):

    rows = return_table_rows(db, table_name)

    if rows >= config.MAX_ROWS:
        return 1
    else:
        return 0


def insert_check(db, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date):

    if db:
        if message_id:
            if from_chat_id:
                if file_id_1:
                    if file_id_2:
                        if file_id_3:
                            if date:
                                return 0

    return 1


def insert_mysql(db, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date):

    if insert_check(db, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date) == 1:
        return

    cursor = db.cursor()

    # init the config.NU_RANDOM
    get_max_tables()

    all_full = True
    # Here we use the file_id_1 to check the same in mysql
    if check_same_value(db, file_id_1) == 1:
        print('There is full')
        return 0

    for i in range(0, config.NU_RANDOM):
        # logging.debug(">>>>>>>>>>>>>>>>>>>>>>>>{}".format(i))
        # we check all the database is full or not
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        if check_table_full(db, table_name) == 1:
            # rows > config.MAX_ROWS
            continue
        else:
            # rows <= config.MAX_ROWS
            # we will insert data into this table
            all_full = False
            # message_id, from_chat_id， file_id_1, file_id_2, file_id_3
            try:
                cursor.execute("INSERT INTO %s(message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                    table_name, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date))
            except Exception as e:
                e = 'insert_mysql() execute-1 failed: ' + str(e.args)
                error_log.write_it(e)
                return 1

    if all_full == True:
        # we will create new table here
        # config.NU_RANDOM is the count of tables
        table_name = "{0}pic_{1}".format(
            config.SQL_FORMAT, config.NU_RANDOM)
        create_new_tables(db, table_name)
        try:
            cursor.execute("INSERT INTO %s(message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                table_name, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date))
        except Exception as e:
            e = 'insert_mysql() execute-2 failed: ' + str(e.args)
            error_log.write_it(e)
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
    # db = connect_mysql()
    dt = datetime.now()
    date = dt.strftime('%Y-%m-%d %I:%M:%S')
    try:
        if insert_mysql(db, in_list[0], in_list[1], in_list[2], in_list[3], in_list[4], date) == 1:
            rollback_mysql(db)
    except Exception as e:
        # IndexError and TypeError
        e = 'process_sql() failed: ' + str(e.args)
        error_log.write_it(e)
        pass


def show_sql_status():

    db = connect_mysql()

    get_max_tables()
    return_list = []

    for i in range(0, config.NU_RANDOM):
        # logging.debug(">>>>>>>>>>>>>>>>>>>>>>>>{}".format(i))
        # we check all the database is full or not
        tmp_list = []
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        rows = return_table_rows(db, table_name)
        tmp_list.append(table_name)
        tmp_list.append(int(rows))
        return_list.append(tmp_list)

    return return_list


def check_sql_existed(file_id_1, file_id_2, file_id_3):

    get_max_tables()
    db = connect_mysql()

    # mid_result = check_mid_existed(db, mid)
    file_1_result = check_file_id_1_existed(db, file_id_1)
    file_2_result = check_file_id_2_existed(db, file_id_2)
    file_3_result = check_file_id_3_existed(db, file_id_3)

    tmp_list = []
    # tmp_list.append(mid_result)
    tmp_list.append(file_1_result)
    tmp_list.append(file_2_result)
    tmp_list.append(file_3_result)
    return tmp_list


def check_mid_existed(db, mid):

    cursor = db.cursor()
    same_count = 0

    for i in range(0, config.NU_RANDOM):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        cursor.execute("SELECT * FROM %s WHERE message_id='%s'" %
                       (table_name, mid))

        result_length = len(cursor.fetchall())
        # we have the same value in MySQL
        same_count = same_count + result_length

    return same_count


def check_file_id_1_existed(db, file_id):

    cursor = db.cursor()
    same_count = 0

    for i in range(0, config.NU_RANDOM):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        cursor.execute("SELECT * FROM %s WHERE file_id_1='%s'" %
                       (table_name, file_id))

        result_length = len(cursor.fetchall())
        # we have the same value in MySQL
        same_count = same_count + result_length

    return same_count


def check_file_id_2_existed(db, file_id):

    cursor = db.cursor()
    same_count = 0

    for i in range(0, config.NU_RANDOM):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        cursor.execute("SELECT * FROM %s WHERE file_id_2='%s'" %
                       (table_name, file_id))

        result_length = len(cursor.fetchall())
        # we have the same value in MySQL
        same_count = same_count + result_length

    return same_count


def check_file_id_3_existed(db, file_id):

    cursor = db.cursor()
    same_count = 0

    for i in range(0, config.NU_RANDOM):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        cursor.execute("SELECT * FROM %s WHERE file_id_3='%s' limit 1" %
                       (table_name, file_id))

        result_length = len(cursor.fetchall())
        # we have the same value in MySQL
        same_count = same_count + result_length

    return same_count
