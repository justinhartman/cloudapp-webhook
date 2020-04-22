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
    git remote add origin https://"${GITHUB_USERNAME}":"${GITHUB_WRITE_REPO}"@github.com/thecreativeacademy/heroku-media.git
    git lfs track "*.mov"
    git lfs track "*.mp4"
    git config --global user.name "Automated GitHub User"
    git config --global user.email "j.hartman@ctca.co.za"
    git pull -f origin master
    git fetch --tags
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
    rm README.md
}

# Run the application thread.
git_setup
cleanup
exit 0
