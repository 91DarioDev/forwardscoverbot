#!/usr/bin/env python3

import os
from datetime import datetime

from hatsunebot import config


def RecordError(input_str):
    '''
    write the error to the /var/log/
    '''

    # get the time
    dt = datetime.now()
    date = dt.strftime('%Y-%m-%d %I:%M:%S')

    try:
        with open(config.ERROR_LOG, 'a+') as fp:
            fp.writelines(date + ': ' + input_str + '\n')
    except Exception as e:
        RecordError(e.args)
