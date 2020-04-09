#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
The main application script.

This script contains all the application code for downloading media from
CloudApp and then uploading them to Google Drive using the Google Drive API.
"""
import time
import app
import db
import downloads
import media
import upload
import utility


def main():
    """Return the main application method."""
    started = time.time()
    utility.timestamp_top()
    # Path the database.
    database = app.DATABASE_PATH
    # create a database connection.
    utility.timestamp_message("Opening the database connection.")
    conn = db.create_connection(database)
    with conn:
        utility.timestamp_message("Getting list of records from database.")
        rows = db.select_all(conn)
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
            if utility.check_path(app.MEDIA_PATH) is False:
                utility.timestamp_message("ERROR: Media folder not valid.")
                return 1

            """
            If no name is set, build a name and check the filetype.
            """
            if name is None:
                # Get file extension from content-type.
                ext = media.get_extension(download_url)
                # Generate a random string.
                ran = utility.random_string()
                # Concatenate the filename with extension.
                new_name = ran + str(ext)
                # Save the new filename in the database.
                db.update_filename(conn, new_name, item_id)
                name = new_name

            """
            Download the file to server.
            """
            utility.timestamp_message("Downloading \"" + name + "\"")
            status, size = downloads.download_file(name, download_url)
            utility.timestamp_message(str(status)+": "+name+" ("+link+")")

            """
            Update database if successfull.
            """
            if status == 200:
                rid = db.insert_record(conn, item_id, size, status)
                utility.timestamp_message(str(rid)+" inserted in downloads.")
                db.update_record(conn, 1, item_id)
                utility.timestamp_message("Updated ID " + str(item_id))

                # Make connection to Google Drive API.
                credentials = upload.get_client()
                # Upload file to API.
                utility.timestamp_message("Uploading to Google Drive.")
                file_id, file_name = upload.upload_media(credentials, name)
                # Insert Upload into DB.
                db.insert_upload(conn, rid, file_id, file_name)
                utility.timestamp_message(file_id+" inserted in uploads.")
            elif status == 404:
                db.update_record(conn, 2, item_id)
                utility.timestamp_message("404 file not found.")
            else:
                print(utility.date_time(2) + " General error")
                utility.timestamp_message("General Unknown Error.")
        else:
            utility.timestamp_message("Closing the database connection.")
    conn.close()
    completed = time.time()
    utility.timestamp_tail(completed, started)

    return bool(1)


if __name__ == '__main__':
    main()
