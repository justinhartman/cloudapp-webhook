#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Media module.

A module containing methods for working with media. These include methods for:
- Building new URLs.
- Get file extension from mime-types.
- Define the save path for media files.
- Define the folder to upload media files to.
"""
import requests
import sys
sys.path.append('../')
import settings
import mime_types


def build_url(url):
    """
    Build a download url.

    :param url: The original url to convert.
    :type  url: string

    :returns: New download url.
    :rtype:   string
    """
    replace = settings.HTTP_URL
    items = "https://media.ctca.co.za/items"
    link = url.replace(replace, items) + "/download"

    return link


def get_extension(url):
    """
    Return a file extension based on mime type.

    :param url: The url to the download file.
    :type  url: string

    :returns: File extension|False
    :rtype:   string|boolean
    """
    file = requests.get(url, allow_redirects=True)

    # Get the content-type header.
    content_type = file.headers['content-type']

    for file_types in mime_types.MIME_TYPES:
        if content_type in file_types:
            return file_types[1]
    # TODO: To fix this else I think I just need to remove else and un-indent
    # the return bool(0) to the same indent level as the for statement.
    # This needs to be tested.
    else:
        return False


def save_path(filename):
    """
    Generate a path to download the file to in downloads module.

    :param filename: The file filename.
    :type  filename: string

    :returns: Full path.
    :rtype:   string
    """
    img = filename.endswith(".png")
    mov = filename.endswith(".mov")
    mp4 = filename.endswith(".mp4")

    if img:
        path = settings.MEDIA_IMAGE
    elif mov:
        path = settings.MEDIA_VIDEO
    elif mp4:
        path = settings.MEDIA_VIDEO
    else:
        path = settings.MEDIA_OTHER

    return path


def file_paths(filename):
    """
    Get local path and remote path from filename for rclone module.

    :param filename: The filename
    :type  filename: string

    :returns: Mixed variables.
    :rtype:   string
    """
    img = filename.endswith(".png")
    mov = filename.endswith(".mov")
    mp4 = filename.endswith(".mp4")

    if img:
        src_path = settings.MEDIA_IMAGE + filename
        drv_path = settings.RCLONE_GDRIVE_IMAGE
    elif mov:
        src_path = settings.MEDIA_VIDEO + filename
        drv_path = settings.RCLONE_GDRIVE_VIDEO
    elif mp4:
        src_path = settings.MEDIA_VIDEO + filename
        drv_path = settings.RCLONE_GDRIVE_VIDEO
    else:
        src_path = settings.MEDIA_OTHER + filename
        drv_path = settings.RCLONE_GDRIVE_OTHER

    return src_path, drv_path
