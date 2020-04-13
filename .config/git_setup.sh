#!/bin/bash
#
# Setup the media folders and SQLite database from repo.
#
# Author: Justin Hartman <j.hartman@ctca.co.za>
# Version: 1.0.0
# Copyright (c) 2020 Creative Academy <https://creativeacademy.ac.za>
#

#######################################
# Setup the repo.
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
#######################################
git_setup () {
    echo "Setting up the Git repo..."
    rm .gitignore
    git init
    git remote add origin https://"${GITLAB_USERNAME}":"${GITLAB_WRITE_REPO}"@gitlab.com/ctca/heroku-media.git
    git config --global user.name "CTCA GitLab Heroku"
    git config --global user.email "ctca-gitlab-heroku@hartman.me"
    git pull origin master
}

#######################################
# Cleanup files not needed.
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
#######################################
cleanup() {
    echo "Performing a cleanup on the server..."
    rm .config/create.sql
    rm database/create.sql
    rm README.md
}

# Run the application thread.
git_setup
cleanup
exit 0
