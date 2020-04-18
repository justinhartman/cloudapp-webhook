#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Downloads module.

A module containing methods for downloading files from CloudApp to the server.
"""
import requests
import subprocess
from media import save_path
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
    path = save_path(name)

    command = ['aria2c', url, '--dir='+path, '--out='+name]
    # command = ['aria2c', url, '--dir='+path]
    process = subprocess.run(
        command,
        check=True,
        text=True
    )

    return name
