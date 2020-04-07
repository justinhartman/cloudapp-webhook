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
    items = "https://media.ctca.co.za/items"
    link = url.replace(replace, items) + "/download"

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


def save_path(filename):
    """
    Generates a full path to download the file to.

    :param filename: The file filename.
    :type  filename: String

    :returns: Full path with filename.
    :rtype:   String
    """
    img = filename.endswith(".png")
    mov = filename.endswith(".mov")
    mp4 = filename.endswith(".mp4")

    if img:
        full_path = app.MEDIA_IMAGE + filename
    elif mov:
        full_path = app.MEDIA_VIDEO + filename
    elif mp4:
        full_path = app.MEDIA_VIDEO + filename
    else:
        full_path = app.MEDIA_OTHER + filename

    return full_path


def get_file_type(filename):
    """
    Get file type from filename.

    :param filename: The filename
    :type  filename: String

    :returns: file_type|folder_id
    :rtype:   String|String
    """
    img = filename.endswith(".png")
    mov = filename.endswith(".mov")
    mp4 = filename.endswith(".mp4")

    if img:
        file_type = "image/png"
        folder_id = app.DRIVE_IMAGE_FOLDER
    elif mov:
        file_type = "video/quicktime"
        folder_id = app.DRIVE_VIDEO_FOLDER
    elif mp4:
        file_type = "video/mp4"
        folder_id = app.DRIVE_VIDEO_FOLDER
    else:
        file_type = "application/octet-stream"
        folder_id = app.DRIVE_OTHER_FOLDER

    return file_type, folder_id
