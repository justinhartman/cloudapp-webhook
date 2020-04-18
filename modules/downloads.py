#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Downloads module.

A module containing methods for downloading files from CloudApp to the server.
"""
import requests
import subprocess
from media import save_path, aria_save_path
from utility import Utility


def aria_download(name, url):
    """
    Download a file.
    e.g.: aria2c https://example.com/go.mov --dir=/app/media/other --out=go.mov

    :param name: The file name.
    :type  name: string
    :param url:  The url to download a file.
    :type  url:  string

    :returns: void
    :rtype:   bool
    """
    path = aria_save_path(name)

    command = ['aria2c', url, '--dir='+path, '--out='+name]
    # command = ['aria2c', url, '--dir='+path]
    process = subprocess.run(
        command,
        check=True,
        text=True
    )

    return name
    


def download_file(name, url):
    """
    Download a file.

    :param name: The file name.
    :type  name: string
    :param url:  The url to download a file.
    :type  url:  string

    :returns: file_status|file_size
    :rtype:   integer|string
    """
    utl = Utility()
    path = save_path(name)
    file = requests.get(url, allow_redirects=True)

    # Get the file status.
    file_status = file.status_code

    if file_status == 404:
        file_size = '0'
    elif file_status in (200, 302):
        length = float(file.headers['Content-Length'])
        file_size = utl.convert_size(length)

        # Save the file in chunks.
        with open(path, 'wb') as chunks:
            for chunk in file.iter_content(chunk_size=128):
                chunks.write(chunk)

        print(utl.date_time(2) + " Downloaded " + file_size)
    else:
        file_status = 0
        file_size = '0'

    return file_status, file_size
