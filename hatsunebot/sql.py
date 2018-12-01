#!/usr/bin/env python3

import pymysql
import logging
import sys
import random
from datetime import datetime

from hatsunebot import config
from hatsunebot import error_log

from telegram import ParseMode


def SQL_GetMaxTableCount():

    db = SQL_ConnectMysql()
    cursor = db.cursor()
    # get how many tables we have in the database
    cursor.execute(
        "SELECT table_rows FROM information_schema.tables WHERE table_schema='%s'" % config.SQL_DATABASE)
    rows = cursor.fetchall()
    config.NU_RANDOM = len(rows)
    SQL_Close(db)


def SQL_GetFid(db, table_name, mid):

    cursor = db.cursor()
    fid = None
    while fid == None:
        cursor.execute(
            "SELECT from_chat_id FROM %s WHERE message_id='%s'" % (table_name, mid))
        fid = cursor.fetchone()[0]

    # print(">>>>>>>>>>>>>>>>>>>>>>>>>{}".format(fid))
    return fid


def SQL_IterationAllData(db, table_name, update):
    '''
    here we work
    '''

    cursor = db.cursor()
    count_list = []

    cursor.execute(
        "SELECT table_rows FROM information_schema.tables WHERE table_name='%s'" % table_name)

    rows = cursor.fetchone()[0]
    # print(rows)
    cursor.execute("SELECT * FROM %s" % table_name)
    data_tuple = cursor.fetchall()
    # print(data_tuple)
    show_time = 1000
    i = 1

    for r in range(0, rows):

        if show_time < 1:
            show_time = 1000
            text = '<b>Checking the %d down</b>' % (i * 1000)
            update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
            i += 1

        # every rows will here
        # print(data_tuple[r])
        file_id_1 = data_tuple[r][2]
        count_1 = SQL_CheckFile1Existed(db, file_id_1)
        file_id_2 = data_tuple[r][3]
        count_2 = SQL_CheckFile2Existed(db, file_id_2)
        file_id_3 = data_tuple[r][4]
        count_3 = SQL_CheckFile3Existed(db, file_id_3)

        if count_1 == count_2 and count_2 == count_3:
            if count_1 > 1:
                config.CHECK_FILE_ID_LIST.append(file_id_1)
                count_list.append(count_1)
        else:
            pass

        show_time -= 1

    return count_list


def SQL_GetMidLimited(db, table_name):

    cursor = db.cursor()
    #mid = -1
    # clear the list
    config.MID_LIST = []
    rows = None
    fall = None

    cursor.execute(
        "SELECT table_rows FROM information_schema.tables WHERE table_name='%s'" % table_name)
    while rows == None:
        try:
            rows = cursor.fetchone()[0]
        except TypeError:
            pass
    # print(rows)
    random_limit_row_max = random.randint(0, int(rows))
    # pick up 1000 items from mysql
    if random_limit_row_max - config.MAX_MID_LIST > 0:
        random_limit_row_min = random_limit_row_max - config.MAX_MID_LIST
    else:
        random_limit_row_min = random_limit_row_max
        random_limit_row_max = random_limit_row_max + config.MAX_MID_LIST

    cursor.execute("SELECT message_id FROM %s LIMIT %d, %d" %
                   (table_name, random_limit_row_min, random_limit_row_max))

    while fall == None:
        fall = cursor.fetchall()

    config.MID_LIST.append(fall)

    while len(config.MID_LIST) == 0:
        SQL_GetMidLimited(db, table_name)

    # print(len(config.MID_LIST))
    # mid = cursor.fetchall()[random_rows][0]
    # return (mid, random_rows)


def SQL_GetMysqlVersion(db):

    cursor = db.cursor()
    cursor.execute("SELECT version()")
    return cursor.fetchone()[0]


def SQL_CreateNewTable(db, table_name):

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
        error_log.RecordError(e)
        return 1


def SQL_ConnectMysql():

    # now connect to msyql
    try:
        db = pymysql.connect(config.SQL_SERVER, config.SQL_USER,
                             config.SQL_PASSWORD, config.SQL_DATABASE)
        # logging.debug("Connect to {}".format(get_mysql_version(db)))
        return db
    except Exception:
        logging.error("Can't connected to mysql server...")
        sys.exit(1)


def SQL_GetTablesRow(db, table_name):

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


def SQL_CheckTableFullOrNot(db, table_name):

    rows = SQL_GetTablesRow(db, table_name)

    if rows >= config.MAX_ROWS:
        return 1
    else:
        return 0


def SQL_InsertCheck(db, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date):

    if db:
        if message_id:
            if from_chat_id:
                if file_id_1:
                    if file_id_2:
                        if file_id_3:
                            if date:
                                return 0

    return 1


def SQL_CheckSameValue(db, file_id):

    SQL_GetMaxTableCount()
    cursor = db.cursor()
    for i in range(0, config.NU_RANDOM):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        cursor.execute("SELECT * FROM %s WHERE file_id_1='%s' LIMIT 1" %
                       (table_name, file_id))
        if cursor.fetchone() != None:
            # we have the same value in MySQL
            # so we return 1
            return 1
    return 0


def SQL_InsertMysql(db, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date):

    if SQL_InsertCheck(db, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date) == 1:
        return

    cursor = db.cursor()

    # init the config.NU_RANDOM
    SQL_GetMaxTableCount()

    all_full = True
    # Here we use the file_id_1 to check the same in mysql
    if SQL_CheckSameValue(db, file_id_1) == 1:
        # print('same value')
        # we have the same value in MySQL
        return 0

    for i in range(0, config.NU_RANDOM):
        # logging.debug(">>>>>>>>>>>>>>>>>>>>>>>>{}".format(i))
        # we check all the database is full or not
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        if SQL_CheckTableFullOrNot(db, table_name) == 1:
            # rows > config.MAX_ROWS
            continue
        else:
            # rows <= config.MAX_ROWS
            # we will insert data into this table
            all_full = False
            # message_id, from_chat_id, file_id_1, file_id_2, file_id_3
            try:
                cursor.execute("INSERT INTO %s(message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                    table_name, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date))
                # commit_mysql(db)
            except Exception as e:
                e = 'insert_mysql() execute-1 failed: ' + str(e.args)
                error_log.RecordError(e)
                return 1

    if all_full == True:
        # we will create new table here
        # config.NU_RANDOM is the count of tables
        table_name = "{0}pic_{1}".format(
            config.SQL_FORMAT, config.NU_RANDOM)
        SQL_CreateNewTable(db, table_name)
        try:
            cursor.execute("INSERT INTO %s(message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                table_name, message_id, from_chat_id, file_id_1, file_id_2, file_id_3, date))
        except Exception as e:
            e = 'insert_mysql() execute-2 failed: ' + str(e.args)
            error_log.RecordError(e)
            return 1
    return 0


def SQL_Commit(db):

    db.commit()


def SQL_RollBack(db):

    db.rollback()


def SQL_Close(db):

    # logging.debug('Close mysql connection')
    db.close()


def SQL_Process(db, in_list):

    #            0              1           2          3           4
    # LIST = [MESSAGE_ID, FROM_CHAT_ID， FILE_ID_1, FILE_ID_2, FILE_ID_3]
    # db = connect_mysql()
    dt = datetime.now()
    date = dt.strftime('%Y-%m-%d %I:%M:%S')
    try:
        if SQL_InsertMysql(db, in_list[0], in_list[1], in_list[2], in_list[3], in_list[4], date) == 1:
            SQL_RollBack(db)
    except Exception as e:
        # IndexError and TypeError
        e = 'process_sql() failed: ' + str(e.args)
        error_log.RecordError(e)
        pass


def SQL_ShowStatus():

    db = SQL_ConnectMysql()

    SQL_GetMaxTableCount()
    return_list = []

    for i in range(0, config.NU_RANDOM):
        # logging.debug(">>>>>>>>>>>>>>>>>>>>>>>>{}".format(i))
        # we check all the database is full or not
        tmp_list = []
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        rows = SQL_GetTablesRow(db, table_name)
        tmp_list.append(table_name)
        tmp_list.append(int(rows))
        return_list.append(tmp_list)

    return return_list


def SQL_CheckExisted(file_id_1, file_id_2, file_id_3):

    SQL_GetMaxTableCount()
    db = SQL_ConnectMysql()

    # mid_result = check_mid_existed(db, mid)
    file_1_result = SQL_CheckFile1Existed(db, file_id_1)
    file_2_result = SQL_CheckFile2Existed(db, file_id_2)
    file_3_result = SQL_CheckFile3Existed(db, file_id_3)

    tmp_list = []
    # tmp_list.append(mid_result)
    tmp_list.append(file_1_result)
    tmp_list.append(file_2_result)
    tmp_list.append(file_3_result)

    SQL_Close(db)
    return tmp_list


def SQL_CheckMidExisted(db, mid):

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


def SQL_CheckFile1Existed(db, file_id):

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


def SQL_CheckFile2Existed(db, file_id):

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


def SQL_CheckFile3Existed(db, file_id):

    cursor = db.cursor()
    same_count = 0

    for i in range(0, config.NU_RANDOM):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        cursor.execute("SELECT * FROM %s WHERE file_id_3='%s'" %
                       (table_name, file_id))

        result_length = len(cursor.fetchall())
        # we have the same value in MySQL
        same_count = same_count + result_length

    return same_count


def SQL_DeleteOneValue(cursor, table_name, file_id):

    cursor.execute("DELETE FROM %s WHERE file_id_1='%s' LIMIT 1" %
                   (table_name, file_id))


def SQL_DeleteSameValue(file_id):

    SQL_GetMaxTableCount()

    db = SQL_ConnectMysql()
    cursor = db.cursor()

    for i in range(0, config.NU_RANDOM):
        table_name = "{0}pic_{1}".format(config.SQL_FORMAT, i)
        while SQL_CheckFile1Existed(db, file_id) > 1:
            # print('delete')
            SQL_DeleteOneValue(cursor, table_name, file_id)
            SQL_Commit(db)

    SQL_Close(db)
