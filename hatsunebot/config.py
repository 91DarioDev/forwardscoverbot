#!/usr/bin/env python3

import yaml
import sys
import logging


path = "config/config.yaml"
if len(sys.argv) == 2:
    path = sys.argv[1]
try:
    with open(path, 'r') as stream:
        conf = yaml.load(stream)
except IOError:
    print("\nWARNING:\n"
          "before of running this bot you should create a file named `config.yaml` in `config`"
          ".\n\nOpen `config/config.example.yaml`"
          "\ncopy all"
          "\ncreate a file named `config.yaml`"
          "\nPaste and replace sample variables with true data."
          "\nIf the file is in another path, you can specify it as the first parameter.")
    sys.exit()

BOT_TOKEN = conf["bot_token"]
#logging.info("BOT TOKEN: {}".format(BOT_TOKEN))
ADMINS = conf["admins"]
#logging.info("ADMINS: {}".format(ADMINS))
ADMINS_GROUP = conf["admins_group"]
#logging.info("ADMINS GROUP: {}".format(ADMINS_GROUP))
CHAT_ID = conf["chat_id"]
#logging.info("CHAT ID: {}".format(CHAT_ID))

ERROR_LOG = conf["error_log_location"]

# MESSAGE_ID_LIST = []
# FROM_CHAT_ID_LIST = []
# FIVE_TYPE_LIST = [[MESSAGE_ID, FROM_CHAT_ID， FILE_ID_1, FILE_ID_2, FILE_ID_3], [MESSAGE_ID, FROM_CHAT_ID, FILE_ID, FILE_ID_2, FILE_ID_3]]
FIVE_TYPE_LIST = []
FIVE_TYPE_LIST_MAX_LENGTH = 5
FIVE_TYPE_LIST_MIN_LENGTH = 2
# PHOTO_FILE_ID = []
# structure same as FIVE_TYPE_LIST
SQL_LIST = []

# set the sql status
SQL_STATUS = True
FORWARD_STATUS = True

SQL_SERVER = conf["sql_server"]
#logging.info("MYSQL SERVER ADDRESS: {}".format(SQL_SERVER))
SQL_USER = conf["sql_user"]
#logging.info("MYSQL USER: {}".format(SQL_USER))
SQL_PASSWORD = conf["sql_password"]
#logging.info("MYSQL PASSWORD: ********")
SQL_DATABASE = conf["sql_database"]
#logging.info("MYSQL DATABASE: {}".format(SQL_DATABASE))
SQL_FORMAT = conf["sql_format"]
#logging.info("MYSQL FORMAT: {}".format(SQL_FORMAT))
MAX_ROWS = int(conf["max_rows"])
#logging.info("MYSQL MAX ROWS: {}".format(MAX_ROWS))

NU_RANDOM = 0
# every 5 minutes clean up this list avoid sends the same photos once
LAST_MESSAGE_ID_LIST = []
# ALBUM_DICT = {}
# CONFLICT_LIST = []
CHECK_STATUS = False
# CHECK_LIST = []
# CHECK_REPLY_CID = 0
