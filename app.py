#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Application configuration file.

A series of constants and module imports for reuse in the application.
"""
import sys
sys.path.append('./modules')
"""
General.
"""
APP_HOME = '/srv/data/web/vhosts/cloudapp.hartman.me/htdocs/'
# APP_HOME = './'
GOOGLE_CREDENTIALS = APP_HOME + 'credentials.json'
"""
Python Packages.
"""
GOOGLE_PACKAGES = '/home/hosting-user/.local/lib/python3.5/site-packages/'
LOCAL_PACKAGES = APP_HOME + 'modules/'
"""
Media files.
"""
MEDIA_PATH = APP_HOME + 'media/'
MEDIA_IMAGE = MEDIA_PATH + 'images/'
MEDIA_OTHER = MEDIA_PATH + 'other/'
MEDIA_VIDEO = MEDIA_PATH + 'videos/'
HTTP_URL = 'https://media.ctca.co.za'
DATABASE_PATH = APP_HOME + 'database/database.sqlite'
"""
Google Drive constants.
"""
DRIVE_MEDIA_FOLDER = '0AMzDjXZ2bebtUk9PVA'
DRIVE_IMAGE_FOLDER = '1qCEMCqW5gveSArD5k7W_1Q-FWY4mvV7S'
DRIVE_VIDEO_FOLDER = '1DClecbZXR2LIjEeS4S9zr5PBueP7ovrx'
DRIVE_OTHER_FOLDER = '1opGMRZej3qYVxkYSR8FCWCdfl0pG6EWR'
