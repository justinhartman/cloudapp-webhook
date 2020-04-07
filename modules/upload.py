#!/usr/bin/env python3
import sys
sys.path.append('../')
import app
sys.path.append(app.GOOGLE_PACKAGES)
import json
# import media
from apiclient import discovery, errors
from httplib2 import Http
# from oauth2client import client, file, tools
from apiclient.http import MediaFileUpload

def get_client():
    from google.oauth2 import service_account
    import googleapiclient.discovery

    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = './credentials.json'
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    return credentials

# define a function to retrieve all files
def retrieve_all_files(api_service):
    results = []
    page_token = None

    while True:
        try:
            param = {}

            if page_token:
                param['pageToken'] = page_token

            files = api_service.files().list(**param).execute()
            # append the files from the current result page to our list
            results.extend(files.get('files'))
            # Google Drive API shows our files in multiple pages when the number of files exceed 100
            page_token = files.get('nextPageToken')

            if not page_token:
                break

        except errors.HttpError as error:
            print(f'An error has occurred: {error}')
            break
    # output the file metadata to console
    for file in results:
        print(file)

    return results


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
