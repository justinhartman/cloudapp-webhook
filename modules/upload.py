#!/usr/bin/env python3
import sys
sys.path.append('../')
import app
sys.path.append(app.GOOGLE_PACKAGES)
from apiclient import discovery
from apiclient.http import MediaFileUpload


def get_client():
    from google.oauth2 import service_account

    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = './credentials.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    return credentials


def upload_media(credentials, filename):
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
