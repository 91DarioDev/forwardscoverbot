#!/usr/bin/env python3

import yaml
import sys


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
ADMINS = conf["admins"]
CHAT_ID = conf["chat_id"]

#MESSAGE_ID_LIST = []
#FROM_CHAT_ID_LIST = []
PHOTO_FILE_ID = []

# set the sql status
SQL_STATUS = True
FORWARD_STATUS = True

SQL_SERVER = conf["sql_server"]
SQL_USER = conf["sql_user"]
SQL_PASSWORD = conf["sql_password"]
SQL_DATABASE = conf["sql_database"]
SQL_FORMAT = conf["sql_format"]
MAX_ROWS = int(conf["max_rows"])

NU_RANDOM = 0
ALBUM_DICT = {}
