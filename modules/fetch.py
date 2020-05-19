#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Fetch script.

Script executes the main app and commits file addition and changes to the
GitHub repository.
"""
import git
from utility import Utility


def main():
    """
    Runs the ./bin/main app script which downloads media to the server, updates
    the database with the records and then pushes the media to Google Drive.

    :returns: Status of the execution.
    :rtype:   boolean
    """
    """Setup the Utility class."""
    utl = Utility()

    """cd into the /app directory."""
    command = ['cd', '/app/']
    utl.sub_process(command)

    """Fetch latest files."""
    utl.timestamp_message("🟢 Fetching latest repo changes.")
    git.git_pull()

    """Run the main.py script."""
    utl.timestamp_message("🟢 Executing ./bin/main")
    command = ['./bin/main', '>>', './logs/app.log']
    utl.sub_process(command)

    """Commit files to media repo."""
    utl.timestamp_message("🟢 Committing db and log files to repo.")
    git.git_commit()

    utl.timestamp_message("🟢 Done.")
    return True


if __name__ == '__main__':
    main()
