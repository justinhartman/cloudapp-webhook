#!/usr/bin/env python3
import sys
sys.path.append('../')
import app
import mime_types
import requests


def build_url(url):
    """
    Builds a download url.

    :param url: The original url to convert.
    :type  url: String

    :returns: New download url.
    :rtype:   String
    """
    replace = app.HTTP_URL
    payload = url.replace(replace, '')

    link = app.HTTP_URL + '/items/' + payload + '/download'

    return link


def get_extension(url):
    """
    Returns file extension based on mime type.

    :param url: The url to the download file.
    :type  url: string

    :returns: File extension|False
    :rtype:   string|boolean
    """
    file = requests.get(url, allow_redirects=True)

    # Get the content-type header.
    content_type = file.headers['content-type']

    for a in mime_types.types:
        if content_type in a:
            return a[1]
    else:
        return bool(0)


def save_path(name):
    """
    Generates a full path to download the file to.

    :param name: The file name.
    :type  name: String

    :returns: Full path with filename.
    :rtype:   String
    """
    if '.png' in name:
        full_path = app.MEDIA_IMAGE + name
    elif '.mov' in name:
        full_path = app.MEDIA_VIDEO + name
    else:
        full_path = app.MEDIA_OTHER + name

    return full_path
