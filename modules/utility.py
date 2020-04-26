#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Utility module.

A module containing various utility methods used in the application.
"""
import math
import os.path
import random
import string
import subprocess
import time
from datetime import datetime, timedelta

import requests


class Utility:
    def check_path(self, path):
        """
        Check the path to the media folder exists.

        :param path: Path to check.
        :type  path: string

        :returns: True or false.
        :rtype:   boolean
        """
        check = os.path.exists(path)

        return check

    def convert_size(self, size_bytes):
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

    def date_time(self, offset=0):
        """
        Return a formatted current date and time.

        :param offset: An offset to accommodate for any server time differences
                       Defaults to zero if no param set.
        :type  offset: integer

        :returns: Date formatted like 2020-04-08 09:25:07.
        :rtype:   string
        """
        today = datetime.now() + timedelta(hours=offset)
        formatted = today.strftime('%F %T')
        string = '🕜 ' + formatted

        return string

    def random_string(self, size=32):
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

    def timestamp_top(self):
        """
        Return a header for the log file.

        :returns: Multiple information lines.
        :rtype:   string
        """
        head = '================================================================================'
        subj = "🐍 CloudApp/Google Drive Python Script Log"
        line = '--------------------------------------------------------------------------------'
        build = print(head), print(subj), print(line)

        return build

    def timestamp_message(self, message):
        """
        Return a formatted log file entry with date and time.

        :param message: The message to include in the log file.
        :type  message: object

        :returns: Formatted log file message.
        :rtype:   string
        """
        clean = str(message)
        build = Utility.date_time(self, 2) + " :~$ " + clean
        message = print(build)

        return message

    def timestamp_tail(self, end, start):
        """
        Return a footer containing the time to run script for the log file.

        :param end:   The time the script ended.
        :type  end:   object
        :param start: The time the script started.
        :type  start: object

        :returns: Multiple information lines.
        :rtype:   string
        """
        value = Utility.time_formatter(self, end, start)
        head = '================================================================================'
        subj = "⌛️ Completed in  %d min %d seconds to run." % (value[2], value[3])
        line = '--------------------------------------------------------------------------------'
        build = print(line), print(subj), print(head)
        # build = head, subj, line
        # message = print(build)

        return build

    def time_to_seconds(self, datetime_string):
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

    def time_formatter(self, older, newer):
        """
        Convert two time floats from seconds into day, hour, minute and seconds

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

    def media(self, url):
        """
        Checks the status and size of a file and gets the full download path to
        the media file.

        :param url:  The url to the CloudApp file.
        :type  url:  string

        :returns: file_status|file_size|file_link
        :rtype:   integer|string|string
        """
        media = requests.head(url)
        file = requests.head(url, allow_redirects=True)

        # Get the file status.
        file_status = file.status_code

        # Make sure the file is valid.
        if file_status == 200:
            file_link = media.headers['location']
            file_size = file.headers['Content-Length']
        else:
            file_link = False
            file_size = False

        return file_status, file_size, file_link

    def sub_process(self, command):
        """
        Runs commands using Python subprocess module.

        :param command:  The command to execute.
        :type  command:  array

        :returns: Results|Exception
        :rtype:   mixed|boolean
        """
        try:
            subprocess.run(
                command,
                check=True,
                text=True
            )
        except:
            return False
