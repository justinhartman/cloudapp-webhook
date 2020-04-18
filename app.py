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
# APP_HOME = './'
APP_HOME = '/app/'
APP_CONF = APP_HOME + '.config/'
APP_TIMEZONE = 'Africa/Johannesburg'
"""
Security
"""
GOOGLE_CREDENTIALS = APP_CONF + 'heroku.json'

"""
Python Packages.
"""
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
"""
Rclone Drive values.
"""
RCLONE_GDRIVE_IMAGE = 'gdrive:1. CloudApp Images'
RCLONE_GDRIVE_VIDEO = 'gdrive:2. CloudApp Videos'
RCLONE_GDRIVE_OTHER = 'gdrive:3. CloudApp Uncategorised'
