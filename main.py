#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
The main application script.

This script contains all the application code for downloading media from
CloudApp and then uploading them to Google Drive using the Google Drive API.
"""
import time
import app
from db import Db
import downloads
import media
import upload
from utility import Utility


def main():
    """Return the main application method."""
    started = time.time()
    utl = Utility()
    utl.timestamp_top()
    # create a database connection.
    utl.timestamp_message("Opening the database connection.")
    con = Db()
    utl.timestamp_message("Getting list of records from database.")
    rows = con.select_all()
    for row in rows:
        """
        Define some variables to reuse.
        """
        # Row data.
        item_id = row[0]
        name = row[1]
        link = row[2]
        # Generate a download URL from the link variable.
        download_url = media.build_url(link)

        """
        Make sure the media folder actually exists.
        """
        if utl.check_path(app.MEDIA_PATH) is False:
            utl.timestamp_message("ERROR: Media folder not valid.")
            return bool(0)

        """
        If no name is set, build a name and check the filetype.
        """
        if name is None:
            # Get file extension from content-type.
            ext = media.get_extension(download_url)
            # Generate a random string.
            ran = utl.random_string()
            # Concatenate the filename with extension.
            new_name = ran + str(ext)
            # Save the new filename in the database.
            con.update_filename(new_name, item_id)
            name = new_name

        """
        Download the file to server.
        """
        utl.timestamp_message("Downloading \"" + name + "\"")
        status, size = downloads.download_file(name, download_url)
        utl.timestamp_message(str(status)+": "+name+" ("+link+")")

        """
        Update database if successfull.
        """
        if status == 200:
            rid = con.insert_record(item_id, size, status)
            utl.timestamp_message(str(rid)+" inserted in downloads.")
            con.update_record(1, item_id)
            utl.timestamp_message("Updated ID " + str(item_id))

            # Make conection to Google Drive API.
            credentials = upload.get_client()
            # Upload file to API.
            utl.timestamp_message("Uploading to Google Drive.")
            file_id, file_name = upload.upload_media(credentials, name)
            # Insert Upload into DB.
            con.insert_upload(rid, file_id, file_name)
            utl.timestamp_message(file_id+" inserted in uploads.")
        elif status == 404:
            con.update_record(2, item_id)
            utl.timestamp_message("404 file not found.")
        else:
            print(utl.date_time(2) + " General error")
            utl.timestamp_message("General Unknown Error.")
    else:
        utl.timestamp_message("Closing the database connection.")

    completed = time.time()
    utl.timestamp_tail(completed, started)

    return bool(1)


if __name__ == '__main__':
    main()
