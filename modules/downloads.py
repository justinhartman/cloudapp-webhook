#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Downloads module.

A module containing methods for downloading files from CloudApp to the server.
"""
import requests
import media
import utility


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
    path = media.save_path(name)
    file = requests.get(url, allow_redirects=True)

    # Get the file status.
    file_status = file.status_code

    if file_status == 404:
        file_size = '0'
    elif file_status in (200, 302):
        length = float(file.headers['Content-Length'])
        file_size = utility.convert_size(length)

        # Save the file in chunks.
        with open(path, 'wb') as chunks:
            for chunk in file.iter_content(chunk_size=128):
                chunks.write(chunk)

        print(utility.date_time(2) + " Downloaded " + file_size)
    else:
        file_status = 0
        file_size = '0'

    return file_status, file_size
