#!/bin/bash
#
# Cron job script to commit files to the repo.
# /app/main.py >> /app/logs/python.log && /app/bin/cron_commit.sh
#
# Author: Justin Hartman <j.hartman@ctca.co.za>
# Version: 1.0.0
# Copyright (c) 2020 Creative Academy <https://creativeacademy.ac.za>
#

#######################################
# Commit file changes to repo.
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
#######################################
commit_db () {
    git add database logs
    git commit -m "Automated: Cronjob commit."
    git push -u origin master

    return
}

commit_db
exit 0
