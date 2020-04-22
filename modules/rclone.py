#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Rclone module.
"""
import subprocess

from media import file_paths
from utility import Utility


def upload_gdrive(filename):
    """
    Upload media to Google Drive using rclone.

    :param filename:    The filename of the upload.
    :type  filename:    string

    :returns: Name of file.
    :rtype:   string
    """
    src_path, dst = file_paths(filename)
    src = 'local:' + src_path
    utl = Utility()

    command = ['rclone', 'copy', '-P', src, dst]
    utl.sub_process(command)

    return filename


def upload_gandi(filename):
    # Code here
    return True
