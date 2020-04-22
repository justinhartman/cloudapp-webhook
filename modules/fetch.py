#!/usr/bin/env python3
#
# Webhook script to commit files to the repo.
#
# Author: Justin Hartman <j.hartman@ctca.co.za>
# Version: 1.0.0
# Copyright (c) 2020 Creative Academy <https://creativeacademy.ac.za>
#
import time
# import subprocess
from utility import Utility

utl = Utility()
started = time.time()


# def heroku(util):
#     utl.timestamp_top()
#     utl.timestamp_message("Connecting to Heroku server")
#     command = ['heroku', 'ps:exec', '-a', 'cloudapp-webhooks']
#     utl.sub_process(command)


def fetch(util):
    utl.timestamp_top()
    utl.timestamp_message("Running main script to download media -> sync to drive.")
    command = ['./main', '>>', './logs/python.log']
    utl.sub_process(command)


def commit(util):
    utl.timestamp_message("Git: Adding new files to repository.")
    command = ['git', 'add', 'database', 'logs']
    utl.sub_process(command)

    utl.timestamp_message("Git: Committing files to local repository.")
    command = ['git', 'commit', '-am', 'Automated: Python Fetch script commit.']
    utl.sub_process(command)

    utl.timestamp_message("Git: Pushing local commit to GitHub.")
    command = ['git', 'push', '-u', 'origin', 'master']
    utl.sub_process(command)


# heroku(utl)
fetch(utl)
commit(utl)

completed = time.time()
utl.timestamp_tail(completed, started)
