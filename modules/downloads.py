#!/usr/bin/env python3
import requests
import media
import utility


def download_file(name, url):
    """
    Downloads a file.

    :param name: The file name.
    :type  name: String
    :param url:  The url to download the file.
    :type  url:  String

    :returns: file_status|file_size
    :rtype:   Integer|String
    """
    path = media.save_path(name)
    file = requests.get(url, allow_redirects=True)

    # Get the file status.
    file_status = file.status_code

    if file_status == 404:
        file_size = '0'
    elif file_status == 200 or file_status == 302:
        length = float(file.headers['Content-Length'])
        file_size = utility.convert_size(length)

        # Save the file in chunks.
        with open(path, 'wb') as f:
            for chunk in file.iter_content(chunk_size=128):
                f.write(chunk)

        print(utility.date_time(2) + " Downloaded " + file_size)
    else:
        file_status = 0
        file_size = '0'

    return file_status, file_size
