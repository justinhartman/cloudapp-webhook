#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
The main application script.

This script contains all the application code for downloading media from
CloudApp and then uploading them to Google Drive using the Google Drive API.
"""
import time

import settings
import downloads
import git
import media
import rclone
from db import Db
from utility import Utility


def main():
    """
    Return the main application method.

    :returns: True|Error
    :rtype:   boolean|string
    """
    utl = Utility()
    utl.timestamp_message("🟢 Opening the DB connection.")
    con = Db()
    utl.timestamp_message("🟢 Getting list of records to process from DB.")
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
            utl.timestamp_message("🔴 ERROR: Media folder not valid.")
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
        utl.timestamp_message("🟢 Checking media details for  \"" + name + "\"")
        status, size, download = utl.media(download_url)

        """Download file, Update database and Upload to Drive if successful."""
        if status == 200:
            # Download the file to server.
            utl.timestamp_message("🟢 Downloading \"" + name + "\"")
            downloads.aria_download(name, download)
            utl.timestamp_message("🟢 "+str(status)+": "+name+" ("+link+")")

            # Insert downloaded file to the downloads table.
            rid = con.insert_record(item_id, size, status)
            utl.timestamp_message("📁 "+str(rid)+" inserted in downloads.")

            # Update payload table.
            con.update_record(1, item_id)
            utl.timestamp_message("🟢 Updated ID: " + str(item_id))

            # Upload file to drive.
            utl.timestamp_message("🟢 Uploading to Google Drive.")
            file_name = rclone.upload_gdrive(name)

            # Insert Upload into uploads table.
            con.insert_upload(rid, item_id, file_name)
            utl.timestamp_message("📁 "+file_name+" inserted in uploads.")
        elif status == 404:
            con.update_record(2, item_id)
            utl.timestamp_message("🔴 404 file not found.")
        else:
            utl.timestamp_message("🔴 Unknown Error. ⚠️  " + str(status))
    else:
        utl.timestamp_message("🟢 Finished running.")

    return True


if __name__ == '__main__':
    main()