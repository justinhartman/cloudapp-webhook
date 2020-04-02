#!/usr/bin/env python3
# Import app files.
import constant
import mime_types
# Import system libraries.
import os.path
import requests
import math
import sqlite3
import random
import string
from sqlite3 import Error
from datetime import datetime


def create_connection(db_file):
    """
    Create a database connection to the database specified by the db_file.

    :param db_file: Database file.
    :type  db_file: String

    :returns: Connection object or Error.
    :rtype:   Object
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all(conn):
    """
    Query all rows in the payload table which have to be downloaded.

    :param conn: The Connection.
    :type  conn: Object

    :returns: Array of items.
    :rtype:   Array
    """
    cur = conn.cursor()
    query = "SELECT `id`, `payload_item_name`, `payload_item_url` FROM \
            `payload` WHERE `downloaded` = 0 AND `downloaded_at` IS NULL"
    cur.execute(query)

    rows = cur.fetchall()

    return rows


def select_items(conn, limit):
    """
    Query payload returning a limited number of rows.

    :param conn:  The Connection.
    :type  conn:  Object
    :param limit: The number of records to return.
    :type  limit: Integer

    :returns: item_id|item_name|item_link
    :rtype:   Integer|String|String
    """
    cur = conn.cursor()
    query = "SELECT `id`, `payload_item_name`, `payload_item_url` FROM \
            `payload` WHERE `downloaded` = 0 AND `downloaded_at` IS NULL \
            LIMIT ?"
    cur.execute(query, (limit,))

    rows = cur.fetchall()

    for row in rows:
        item_id = row[0]
        item_name = row[1]
        item_link = row[2]
        return item_id, item_name, item_link
    else:
        print(date_time() + " ERROR: No rows in payload table.")
        return 1


def insert_record(conn, payload_id, file_size, file_status):
    """
    Insert downloaded file details in downloads table.

    :param conn:       The Connection.
    :type  conn:       Object
    :param payload_id: The payload identifier of the record downloaded.
    :type  payload_id: Integer

    :returns: Last row id
    :rtype:   Integer
    """
    cur = conn.cursor()
    query = "INSERT INTO `downloads` (`payload_id`, `file_size`, `status_code`,\
     `created_at`) VALUES (?, ?, ?, strftime('%Y-%m-%d %H:%M:%S', 'now'))"
    cur.execute(query, (payload_id, file_size, file_status,))
    conn.commit()
    insert_id = cur.lastrowid
    cur.close()

    return insert_id


def update_record(conn, status, payload_id):
    """
    Update the downloaded column in the payload table.

    :param conn:       The Connection.
    :type  conn:       Object
    :param status:     The download status.
    :type  status:     Boolean
    :param payload_id: The payload identifier of the record to update.
    :type  payload_id: Integer

    :returns: Payload identifier.
    :rtype:   Integer
    """
    cur = conn.cursor()
    query = "UPDATE `payload` SET `downloaded` = ?, `downloaded_at` = \
            strftime('%Y-%m-%d %H:%M:%S','now') WHERE `id` = ?"
    execute = cur.execute(query, (status, payload_id,))
    conn.commit()
    cur.close()

    return bool(execute)


def update_filename(conn, name, payload_id):
    """
    Update new filename in the payload table.

    :param conn:       The Connection.
    :type  conn:       Object
    :param name:       The new filename.
    :type  name:       Boolean
    :param payload_id: The payload identifier of the record to update.
    :type  payload_id: Integer

    :returns: Payload identifier.
    :rtype:   Integer
    """
    cur = conn.cursor()
    query = "UPDATE `payload` SET `payload_item_name` = ? WHERE `id` = ?"
    cur.execute(query, (name, payload_id,))
    conn.commit()
    cur.close()

    return name


def build_url(url):
    """
    Builds a download url.

    :param url: The original url to convert.
    :type  url: String

    :returns: New download url.
    :rtype:   String
    """
    replace = constant.HTTP_URL
    payload = url.replace(replace, '')

    link = constant.HTTP_URL + '/items/' + payload + '/download'

    return link


def check_path():
    """
    Check the path to the media folder exists.

    :returns: True or false.
    :rtype:   Boolean
    """
    check = os.path.exists(constant.MEDIA_PATH)

    return check


def random_string(size=32):
    """
    Generates a random string.

    :param size: The length of the string to create.
    :type  size: number

    :returns: Random string
    :rtype:   string
    """
    chars = string.ascii_letters + string.digits
    joined = ''.join(random.choice(chars) for x in range(size))

    return joined


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

    for a in mime_types.ARRAY:
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
        full_path = constant.MEDIA_IMAGE + name
    elif '.mov' in name:
        full_path = constant.MEDIA_VIDEO + name
    else:
        full_path = constant.MEDIA_OTHER + name

    return full_path


def convert_size(size_bytes):
    """
    Convert bytes into human readable format.

    :param size_bytes: The size in bytes.
    :type  size_bytes: Integer

    :returns: Human readable format.
    :rtype:   String
    """
    if size_bytes == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)

    return "%s %s" % (s, size_name[i])


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
    path = save_path(name)
    file = requests.get(url, allow_redirects=True)

    # Get the file status.
    file_status = file.status_code

    if file_status == 404:
        file_size = '0'
    elif file_status == 200 or file_status == 302:
        length = float(file.headers['content-length'])
        file_size = convert_size(length)

        # Save file to path.
        # with open(path, 'wb') as f:
        #     f.write(file.content)

        # Save the file in chunks.
        with open(path, 'wb') as f:
            for chunk in file.iter_content(chunk_size=128):
                f.write(chunk)
    else:
        file_status = 0
        file_size = '0'

    return file_status, file_size


def date_time():
    """
    Returns a formatted current date and time.

    :returns: Formatted date time.
    :rtype:   String
    """
    today = datetime.now()
    formatted = today.strftime('%Y-%m-%d %H:%M:%S')

    return formatted


def main():
    print(date_time() + " Starting the downloads.")
    # Path the database.
    database = constant.DATABASE_PATH
    # create a database connection.
    print(date_time() + " Opening the database connection.")
    conn = create_connection(database)
    with conn:
        print(date_time() + " Getting list of records from database.")
        rows = select_all(conn)
        for row in rows:
            """
            Define some variables to reuse.
            """
            # Row data.
            item_id = row[0]
            name = row[1]
            link = row[2]
            # Generate a download URL from the link variable.
            download_url = build_url(link)

            """
            Make sure the media folder actually exists.
            """
            if check_path() is False:
                print(date_time() + " ERROR: Media folder is not accessible.")
                return 1

            """
            If no name is set, build a name and check the filetype.
            """
            if name is None:
                # Get file extension from content-type.
                ext = get_extension(download_url)
                # Generate a random string.
                ran = random_string()
                # Concatenate the filename with extension.
                new_name = ran + str(ext)
                # Save the new filename in the database.
                update_filename(conn, new_name, item_id)
                name = new_name

            """
            Download the file to server.
            """
            status, size = download_file(name, download_url)
            print(date_time()+" "+str(status)+" File: "+name+" URL: "+link)

            """
            Update database if successfull.
            """
            if status == 200:
                insert_record(conn, item_id, size, status)
                print(date_time()+" "+name+" inserted to downloads.")
                update_record(conn, 1, item_id)
                print(date_time()+" Updated id "+str(item_id)+" in payload.")
            elif status == 404:
                update_record(conn, 2, item_id)
                print(date_time() + " 404 file not found.")
            else:
                print(date_time() + " General error")
        else:
            return 0
    print(date_time() + " Closing the database connection.")
    conn.close()

    print(date_time() + " Completed the downloads.")
    return 0

if __name__ == '__main__':
    main()
