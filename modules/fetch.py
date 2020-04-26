#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Fetch script.

Script executes the main app and commits file addition and changes to the
GitHub repository.
"""
import time

import git
from utility import Utility


def main():
    """
    Runs the ./bin/main app script which downloads media to the server, updates
    the database with the records and then pushes all the media to Google Drive.

    :returns: Status of the execution.
    :rtype:   boolean
    """
    # Setup the Utility class and start the timer.
    utl = Utility()
    started = time.time()

    # cd into the /app directory.
    utl.timestamp_top()
    command = ['cd', '/app/']
    utl.sub_process(command)

    # Fetch latest files.
    git.git_pull()

    # Run the main.py script.
    utl.timestamp_message("🟢 Executing ./main to Download and Sync to drive.")
    command = ['./bin/main', '>>', './logs/python.log']
    utl.sub_process(command)

    # Commit files to media repo.
    git.git_commit()

    # Stop the timer and output the time took to run the script
    completed = time.time()
    utl.timestamp_tail(completed, started)

    return True


if __name__ == '__main__':
    main()
