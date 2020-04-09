#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Utility module.

A module containing various utility methods used in the application.
"""
from datetime import datetime, timedelta
import math
import os.path
import random
import string
import time


def check_path(path):
    """
    Check the path to the media folder exists.

    :param path: Path to check.
    :type  path: string

    :returns: True or false.
    :rtype:   boolean
    """
    check = os.path.exists(path)

    return check


def convert_size(size_bytes):
    """
    Convert bytes into human readable format.

    :param size_bytes: The size in bytes.
    :type  size_bytes: integer

    :returns: Human readable format.
    :rtype:   string
    """
    if size_bytes == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    size_a = int(math.floor(math.log(size_bytes, 1024)))
    size_b = math.pow(1024, size_a)
    size_c = round(size_bytes / size_b, 2)

    return "%s %s" % (size_c, size_name[size_a])


def date_time(offset=0):
    """
    Return a formatted current date and time.

    :param offset: An offset to accommodate for any server time differences.
                   Defaults to zero if no param set.
    :type  offset: integer

    :returns: Date formatted like 2020-04-08 09:25:07.
    :rtype:   string
    """
    today = datetime.now() + timedelta(hours=offset)
    formatted = today.strftime('%F %T')

    return formatted


def random_string(size=32):
    """
    Generate a random string.

    :param   size: The length of the string to create.
    :type    size: number
    :default size: 32

    :returns: Random string
    :rtype:   string
    """
    chars = string.ascii_letters + string.digits
    joined = ''.join(random.choice(chars) for x in range(size))

    return joined


def timestamp_top():
    """
    Return a header for the log file.

    :returns: Multiple information lines.
    :rtype:   string
    """
    head = '===================================================================\
============='
    subj = "CloudApp/Google Drive Python Script Log"
    line = '-------------------------------------------------------------------\
-------------'
    build = print(head), print(subj), print(line)

    return build


def timestamp_tail(end, start):
    """
    Return a footer containing the time to run script for the log file.

    :param end:   The time the script ended.
    :type  end:   object
    :param start: The time the script started.
    :type  start: object

    :returns: Multiple information lines.
    :rtype:   string
    """
    value = time_formatter(end, start)
    head = '===================================================================\
============='
    subj = "Script took %d min %d seconds to run." % (value[2], value[3])
    line = '-------------------------------------------------------------------\
-------------'
    build = print(line), print(subj), print(head)
    # build = head, subj, line
    # message = print(build)

    return build


def timestamp_message(message):
    """
    Return a formatted log file entry with date and time.

    :param message: The message to include in the log file.
    :type  message: object

    :returns: Formatted log file message.
    :rtype:   string
    """
    clean = str(message)
    build = date_time(2) + " :~$ " + clean
    message = print(build)

    return message


def time_to_seconds(datetime_string):
    """
    Convert a datetime string to a float for converting.

    :param datetime_string: The datetime string
    :type  datetime_string: string

    :returns: Seconds timestamp
    :rtype:   float
    """
    element = datetime.strptime(
        datetime_string,
        "%Y-%m-%d %H:%M:%S"
    )

    time_tuple = element.timetuple()
    timestamp = time.mktime(time_tuple)

    return timestamp


def time_formatter(older, newer):
    """
    Convert two time floats from seconds into day, hour, minute and seconds.

    :param older: The older time.
    :type  older: float
    :param newer: The newer time.
    :type  newer: float

    :returns: Mixed variables for day, hour, minute and second.
    :rtype:   float
    """
    diff = int(older - newer)

    time_float = float(diff)
    day = time_float // (24 * 3600)

    time_float = time_float % (24 * 3600)
    hour = time_float // 3600

    time_float %= 3600
    minutes = time_float // 60

    time_float %= 60
    seconds = time_float

    return day, hour, minutes, seconds
