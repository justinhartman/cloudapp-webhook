#!/bin/bash
#
# Setup the media folders and SQLite database from repo.
#
# Author: Justin Hartman <j.hartman@ctca.co.za>
# Version: 1.0.0
# Copyright (c) 2020 Creative Academy <https://creativeacademy.ac.za>
#

#######################################
# Main application method.
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
#######################################
git_setup () {
    cd /app/ || exit
    # cp .heroku-media/.gitignore /app/
    git init
    git remote add origin https://"${GITLAB_USERNAME}":"${GITLAB_WRITE_REPO}"@gitlab.com/ctca/heroku-media.git
    git config --global user.name "CTCA GitLab Heroku"
    git config --global user.email "ctca-gitlab-heroku@hartman.me"
    git pull origin master
}

# Run the application thread.
git_setup
exit 0
