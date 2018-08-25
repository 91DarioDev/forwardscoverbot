#!/usr/bin/env python3

import os
from datetime import datetime

from hatsunebot import config


def write_it(input_str):
    '''
    write the error to the /var/log/
    '''

    # get the time
    dt = datetime.now()
    date = dt.strftime('%Y-%m-%d %I:%M:%S')

    try:
        with open(config.ERROR_LOG, 'a+') as fp:
            fp.writelines(date + ': ' + input_str)
    except Exception as e:
        write_it(e.args)
