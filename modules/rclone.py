#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Rclone module.
"""
import subprocess
from media import rclone_file_type


def upload_gdrive(filename):
    src_path, dst = rclone_file_type(filename)
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