#!/usr/bin/env python3

import sys
import time

from hatsunebot import messages
from hatsunebot import config


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit()
    arg = sys.argv[1]
    if arg == 'test_mysql':
        file_id = "fahsdjfhaksdhlfkajh"
        db = messages.connect_mysql()
        nu = 0
        while True:
            table_name = "{0}pic_{1}".format(config.SQL_FORMAT, nu)
            check_result = messages.check_mysql_full(db, table_name)
            if check_result == -1:
                nu += 1
                table_name = "{0}pic_{1}".format(config.SQL_FORMAT, nu)
                messages.create_new_tables(db, table_name)
                config.CURRENT_TABLE = table_name
                break

            elif check_result == 0:
                config.CURRENT_TABLE = table_name
                break
            nu += 1

        date = time.asctime(time.localtime(time.time()))
        messages.insert_mysql(db, config.CURRENT_TABLE, file_id, date)
        db.close()
