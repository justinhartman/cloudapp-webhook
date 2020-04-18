#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Rclone module.
"""
import subprocess
from media import file_paths


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

    command = ['rclone', 'copy', '-P', src, dst]
    process = subprocess.run(
        command,
        check=True,
        text=True
    )

    return filename


def upload_gandi(filename):
    # Code here
    return bool(1)
