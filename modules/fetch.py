#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Fetch script.

Script executes the main app and commits file addition and changes to the
GitHub repository.
"""
import git
import log
from utility import Utility


"""Setup the Utility class."""
utl = Utility()


def main():
    """
    Runs the ./bin/main app script which downloads media to the server, updates
    the database with the records and then pushes the media to Google Drive.

    :returns: Status of the execution.
    :rtype:   boolean
    """
    """cd into the /app directory."""
    command = ['cd', '/app/']
    utl.sub_process(command)

    """Fetch latest files."""
    git.git_pull()

    """Run the main.py script."""
    log.doc('info', f"Executing ./bin/main")
    command = ['./bin/main']
    utl.sub_process(command)

    return True


def commit():
    """
    Commit files to media repo.

    :returns: Status of execution.
    :rtype:   boolean
    """
    git.git_commit()

    return True


if __name__ == '__main__':
    main()
    commit()
