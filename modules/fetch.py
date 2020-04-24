#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Fetch script.

Script executes the main app and commits file addition and changes to the
Githhub repository.
"""
import time

from utility import Utility


"""Setup the Utility class and start the timer."""
utl = Utility()
started = time.time()


def fetch(util):
    """
    Runs the ./main app script which downloads media to the server, updates the
    database with the records and then pushes all the media to Google Drive.

    :param util: Utility Class.
    :type  util: object
    """
    utl.timestamp_top()
    command = ['cd', '/app/']
    utl.sub_process(command)

    utl.timestamp_message("✅ Executing ./main to Download and Sync to drive.")
    command = ['./main', '>>', './logs/python.log']
    utl.sub_process(command)


def commit(util):
    """
    Commits the updated database and log files back to the GitHub repo.

    :param util: Utility Class.
    :type  util: object
    """
    utl.timestamp_message("✅ Git: Adding new files to repository.")
    command = ['git', 'add', 'database', 'logs']
    utl.sub_process(command)

    utl.timestamp_message("✅ Git: Committing files to local repository.")
    command = ['git', 'commit', '-am', ':robot: Fetch script commit.']
    utl.sub_process(command)

    utl.timestamp_message("✅ Git: Pushing local commit to GitHub.")
    command = ['git', 'push', '-u', 'origin', 'master']
    utl.sub_process(command)


"""Run the methods."""
fetch(utl)
commit(utl)

"""Stop the timer and output the time took to run the script."""
completed = time.time()
utl.timestamp_tail(completed, started)
