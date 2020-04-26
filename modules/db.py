#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Database module.

This module creates a database connection and contains a series of queries for
use in the application.
"""
import sqlite3
from sqlite3 import Error

from settings import DATABASE_PATH


class Db:
    def create_connection():
        """
        Create a database connection using the location to the database.

        :returns: Connection object or Error.
        :rtype:   object
        """
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
        except Error as e:
            print(e)

        return conn

    def select_all(self):
        """
        Query all rows in the payload table which have to be downloaded.

        :returns: Array of items.
        :rtype:   array
        """
        conn = Db.create_connection()
        cur = conn.cursor()
        query = "SELECT `id`, `payload_item_name`, `payload_item_url` FROM \
                `payload` WHERE `downloaded` = 0 AND `downloaded_at` IS NULL"
        cur.execute(query)

        rows = cur.fetchall()
        cur.close()

        return rows

    def select_items(self, limit):
        """
        Query payload returning a limited number of rows.

        :param limit: The number of records to return.
        :type  limit: integer

        :returns: Array containing ID, name and link.|False
        :rtype:   mixed|boolean
        """
        conn = Db.create_connection()
        cur = conn.cursor()
        query = "SELECT `id`, `payload_item_name`, `payload_item_url` FROM \
                `payload` WHERE `downloaded` = 0 AND `downloaded_at` IS NULL \
                LIMIT 0,?"
        cur.execute(query, (limit,))

        items = []
        rows = cur.fetchall()

        for row in rows:
            item = [row[0], row[1], row[2]]
            items.append(item)

            continue

        cur.close()

        return items

    def select_single(self):
        """
        Query payload returning a single row.

        :returns: Array containing ID, name and link.|False
        :rtype:   mixed|boolean
        """
        conn = Db.create_connection()
        cur = conn.cursor()
        query = "SELECT `id`, `payload_item_name`, `payload_item_url` FROM \
                `payload` WHERE `downloaded` = 0 AND `downloaded_at` IS NULL \
                LIMIT 0,1"
        cur.execute(query,)

        rows = cur.fetchall()

        for row in rows:
            item_id = row[0]
            item_name = row[1]
            item_link = row[2]

        cur.close()

        return item_id, item_name, item_link

    def insert_record(self, payload_id, file_size, file_status):
        """
        Insert downloaded file details in downloads table.

        :param payload_id:  The payload identifier of the record downloaded.
        :type  payload_id:  integer
        :param file_size:   The file size.
        :type  file_size:   string
        :param file_status: The status of the download.
        :type  file_status: string

        :returns: Last row id
        :rtype:   integer
        """
        conn = Db.create_connection()
        cur = conn.cursor()
        query = "INSERT INTO `downloads` (`payload_id`, `file_size`, \
                `status_code`, `created_at`) VALUES (?, ?, ?, \
                strftime('%Y-%m-%d %H:%M:%S', 'now'))"
        cur.execute(query, (payload_id, file_size, file_status,))

        conn.commit()
        insert_id = cur.lastrowid
        cur.close()

        return insert_id

    def insert_upload(self, download_id, drive_id, drive_name):
        """
        Insert downloaded file details in uploads table.

        :param download_id: The payload identifier of the record downloaded.
        :type  download_id: integer
        :param drive_id:    Google Drive folder ID.
        :type  drive_id:    string
        :param drive_name:  The filename.
        :type  drive_name:  string

        :returns: Last row id
        :rtype:   integer
        """
        conn = Db.create_connection()
        cur = conn.cursor()
        query = "INSERT INTO `uploads` (`download_id`, `drive_id`, \
                `drive_name`, `created_at`) VALUES (?, ?, ?, \
                strftime('%Y-%m-%d %H:%M:%S', 'now'))"
        cur.execute(query, (download_id, drive_id, drive_name,))

        conn.commit()
        insert_id = cur.lastrowid
        cur.close()

        return insert_id

    def update_record(self, status, payload_id):
        """
        Update the downloaded column in the payload table.

        :param status:     The download status.
        :type  status:     boolean
        :param payload_id: The payload identifier of the record to update.
        :type  payload_id: integer

        :returns: True/False
        :rtype:   boolean
        """
        conn = Db.create_connection()
        cur = conn.cursor()
        query = "UPDATE `payload` SET `downloaded` = ?, `downloaded_at` = \
                strftime('%Y-%m-%d %H:%M:%S','now') WHERE `id` = ?"
        execute = cur.execute(query, (status, payload_id,))

        conn.commit()
        cur.close()

        return bool(execute)

    def update_filename(self, name, payload_id):
        """
        Update new filename in the payload table.

        :param name:       The new filename.
        :type  name:       boolean
        :param payload_id: The payload identifier of the record to update.
        :type  payload_id: integer

        :returns: Payload identifier.
        :rtype:   integer
        """
        conn = Db.create_connection()
        cur = conn.cursor()
        query = "UPDATE `payload` SET `payload_item_name` = ? WHERE `id` = ?"
        cur.execute(query, (name, payload_id,))

        conn.commit()
        cur.close()

        return name
