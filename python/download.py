import os
import requests
import math
import sqlite3
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
    cur.execute(query, (status, payload_id,))
    cur.close()

    return payload_id


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


def build_url(url):
    """
    Builds a download url.

    :param url: The original url to convert.
    :type  url: String

    :returns: New download url.
    :rtype:   String
    """
    replace = 'https://media.ctca.co.za/'
    payload = url.replace(replace, '')

    link = 'https://media.ctca.co.za/items/' + payload + '/download'

    return link


def save_path(name):
    """
    Generates a full path to download the file to.

    :param name: The file name.
    :type  name: String

    :returns: Full path with filename.
    :rtype:   String
    """
    # os.chdir("/srv/data/web/vhosts/cloudapp.hartman.me/htdocs/media")
    os.chdir('../media')  # localhost

    if '.png' in name:
        path = os.getcwd() + '/images/' + name
    elif '.mov' in name:
        path = os.getcwd() + '/videos/' + name
    else:
        return 0

    return path


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
    elif file_status == 200:
        length = float(file.headers['content-length'])
        file_size = convert_size(length)

        # Save file to path.
        with open(path, 'wb') as f:
            f.write(file.content)
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
    database = r"../database/database.sqlite"
    # create a database connection.
    print(date_time() + " Opening the database connection.")
    conn = create_connection(database)
    with conn:
        print(date_time() + " Getting list of records from database.")
        rows = select_all(conn)
        for row in rows:
            item_id = row[0]
            name = row[1]
            link = row[2]

            # Download the file to server.
            download_url = build_url(link)
            status, size = download_file(name, download_url)
            print(date_time()+" "+str(status)+" File: "+name+" URL: "+link)

            # Update DB if successfull.
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
        # else:
        #     return 0
    print(date_time() + " Closing the database connection.")
    conn.close()

    print(date_time() + " Completed the downloads.")
    return 0

if __name__ == '__main__':
    main()
