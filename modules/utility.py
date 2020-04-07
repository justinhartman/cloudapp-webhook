#!/usr/bin/env python3
from datetime import datetime
import math
import os.path
import random
import string


def check_path(path):
    """
    Check the path to the media folder exists.

    :param path: Path to check.
    :type  path: string

    :returns: True or false.
    :rtype:   Boolean
    """
    check = os.path.exists(path)

    return check


def convert_size(size_bytes):
    """
    Convert bytes into human readable format.

    :param size_bytes: The size in bytes.
    :type  size_bytes: Integer

    :returns: Human readable format.
    :rtype:   String
    """
    if size_bytes == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)

    return "%s %s" % (s, size_name[i])


def date_time():
    """
    Returns a formatted current date and time.

    :returns: Formatted date time.
    :rtype:   String
    """
    today = datetime.now()
    formatted = today.strftime('%Y-%m-%d %H:%M:%S')

    return formatted


def random_string(size=32):
    """
    Generates a random string.

    :param size: The length of the string to create.
    :type  size: number

    :returns: Random string
    :rtype:   string
    """
    chars = string.ascii_letters + string.digits
    joined = ''.join(random.choice(chars) for x in range(size))

    return joined
