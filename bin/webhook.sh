#!/bin/bash
#
# Webhook script to commit files to the repo.
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
    git add *
    git commit -m "Automated: PHP Webhook DB and Logs."
    git push -u origin master

    return
}

commit_db
exit 0
