#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Uploads module.

A module containing methods for uploading files from the server to Google Drive
using the Google Drive API.
"""
import sys
sys.path.append('../')
import app
sys.path.append(app.GOOGLE_PACKAGES)
from apiclient import discovery
from apiclient.http import MediaFileUpload


def get_client():
    """
    Create a Google API connection using a credentials file.

    :returns: Google API Client.
    :rtype:   object
    """
    from google.oauth2 import service_account

    google_scopes = ['https://www.googleapis.com/auth/drive']
    service_account_file = app.GOOGLE_CREDENTIALS
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=google_scopes
    )

    return credentials


def upload_media(credentials, filename):
    """
    Upload media to Google Drive.

    :param credentials: get_client() connection.
    :type  credentials: object
    :param filename:    The filename of the upload.
    :type  filename:    string

    :returns: Array containing ID and name.
    :rtype:   array
    """
    import media
    mime_type, folder_id = media.get_file_type(filename)

    connection = discovery.build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': filename,
        'mimeType': mime_type,
        'parents': [folder_id]
    }

    media = MediaFileUpload(media.save_path(filename),
                            mimetype='application/octet-stream')
    file = connection.files().create(body=file_metadata,
                                     media_body=media,
                                     fields='id,name',
                                     supportsAllDrives=True).execute()

    file_id = file.get('id')
    file_name = file.get('name')

    return file_id, file_name
