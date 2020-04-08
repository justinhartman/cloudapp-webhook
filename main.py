#!/usr/bin/env python3
import app
import db
import downloads
import media
import upload
import utility


def main():
    print('-------------------------------------------------------------------\
-------------')
    print(utility.date_time(2) + " Starting the downloads.")
    # Path the database.
    database = app.DATABASE_PATH
    # create a database connection.
    print(utility.date_time(2) + " Opening the database connection.")
    conn = db.create_connection(database)
    with conn:
        print(utility.date_time(2) + " Getting list of records from database.")
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
                print(utility.date_time(2) + " ERROR: Media folder not valid.")
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
            print(utility.date_time(2) + " Downloading \"" + name + "\"")
            status, size = downloads.download_file(name, download_url)
            print(utility.date_time(2)+" "+str(status)+": "+name+" ("+link+")")

            """
            Update database if successfull.
            """
            if status == 200:
                insert_id = db.insert_record(conn, item_id, size, status)
                print(utility.date_time(2)+" "+str(insert_id)+" inserted in downloads.")
                db.update_record(conn, 1, item_id)
                print(utility.date_time(2)+" Updated id "+str(item_id)+".")

                # Make connection to Google Drive API.
                credentials = upload.get_client()
                # Upload file to API.
                print(utility.date_time(2)+" Uploading to Google Drive.")
                file_id, file_name = upload.upload_media(credentials, name)
                # Insert Upload into DB.
                db.insert_upload(conn, insert_id, file_id, file_name)
                print(utility.date_time(2)+" "+file_id+" inserted in uploads.")
            elif status == 404:
                db.update_record(conn, 2, item_id)
                print(utility.date_time(2) + " 404 file not found.")
            else:
                print(utility.date_time(2) + " General error")
        else:
            print(utility.date_time(2) + " Closing the database connection.")
            print('------------------------------------------------------------\
--------------------')
    conn.close()
    return bool(1)

if __name__ == '__main__':
    main()
