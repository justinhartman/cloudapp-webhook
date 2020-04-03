#!/usr/bin/env python3
import sqlite3
from sqlite3 import Error
import utility


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
        print(utility.date_time() + " ERROR: No rows in payload table.")
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
