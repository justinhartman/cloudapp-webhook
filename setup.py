#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Setup

Setup the application.
"""
from setuptools import setup, find_packages

setup(
    name='CloudApp Drive Webhook',
    version='4.2.0',
    scripts=['./bin/config'],
    packages=find_packages(),
    author='Justin Hartman',
    author_email='j.hartman@ctca.co.za',
    description='This project creates a webhook for CloudApp to upload video and images to the Creative Academy Google Drive API.',
    keywords='google drive cloudapp webhook',
    url='https://cloudapp.ctca.co.za/',
    project_urls={
        'Bug Tracker': 'https://github.com/thecreativeacademy/cloudapp-webhook/issues',
        'Documentation': 'https://github.com/thecreativeacademy/cloudapp-webhook/blob/master/README.md',
        'Source Code': 'https://github.com/thecreativeacademy/cloudapp-webhook.git',
    },
    classifiers=[
        'License :: Copyright :: Cape Town Creative Academy'
    ]
)
