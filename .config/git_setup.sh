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
}

#######################################
# Delete media and database symlinks.
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
#######################################
remove_symlinks() {
    echo "Removing old symlink folders..."
    rm -f media
    rm -f database
}

#######################################
# Run git pull on the repo.
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
#######################################
pull_origin() {
    echo "Pulling the original source code..."
    git pull origin master
}

cleanup() {
    echo "Performing a cleanup on the server..."
    rm .config/create.sql
    rm database/create.sql
    rm README.md
}

# Run the application thread.
git_setup
remove_symlinks
pull_origin
cleanup
exit 0
