#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
The main application script.

This script contains all the application code for downloading media from
CloudApp and then uploading them to Google Drive using the Google Drive API.
"""
import log
import time
import downloads
import media
import rclone
import settings
from db import Db
from utility import Utility


def main():
    """
    Return the main application method.

    :returns: True|Error
    :rtype:   boolean|string
    """
    """Setup the Utility class, start the timer and print log file header."""
    utl = Utility()
    started = time.time()
    log.doc('general', utl.timestamp_top())

    """Setup database connection."""
    log.doc('info', f"Opening the DB connection.")
    con = Db()

    """Get records from database."""
    log.doc('info', f"Getting list of records to process from DB.")
    rows = con.select_all()
    for row in rows:
        """Define variables for reuse."""
        # Row data.
        item_id = row[0]
        name = row[1]
        link = row[2]
        # Generate a download URL from the link variable.
        download_url = media.build_url(link)

        """Make sure the media folder actually exists."""
        if utl.check_path(settings.MEDIA_PATH) is False:
            log.doc('error', f"Media folder not valid.")
            return False

        """If no name is set, build a name and check the filetype."""
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

        """Check status, file size and link of the media url."""
        log.doc('info', f"Checking media details for {name}.")
        status, size, download = utl.media(download_url)

        """Download file, Update database and Upload to Drive if successful."""
        if status == 200:
            # Download the file to server.
            log.doc('info', f"Downloading {name}")
            downloads.aria_download(name, download)
            log.doc('info', f"{status}: {name} ({link})")

            # Insert downloaded file to the downloads table.
            rid = con.insert_record(item_id, size, status)
            log.doc('general', f"📁 {rid} inserted in downloads.")

            # Update payload table.
            con.update_record(1, item_id)
            log.doc('info', f"Updated ID: {item_id}")

            # Upload file to drive.
            log.doc('info', f"Uploading to Google Drive.")
            file_name = rclone.upload_gdrive(name)

            # Insert Upload into uploads table.
            con.insert_upload(rid, item_id, file_name)
            log.doc('general', f"📁 {file_name} inserted in uploads.")
        elif status == 404:
            con.update_record(2, item_id)
            log.doc('error', f"404 file not found.")
        else:
            log.doc('error', f"Unknown Error. ⚠️ {status}.")
    else:
        log.doc('info', f"Finished running.")

    """Stop the timer and output the time took to run the script."""
    completed = time.time()
    log.doc('general', utl.timestamp_tail(completed, started))

    return True


if __name__ == '__main__':
    main()
