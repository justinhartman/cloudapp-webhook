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
    # cd /app/ || exit
    # rm .gitignore
    git init
    git remote add origin https://"${GITLAB_USERNAME}":"${GITLAB_WRITE_REPO}"@gitlab.com/ctca/heroku-media.git
    git config --global user.name "CTCA GitLab Heroku"
    git config --global user.email "ctca-gitlab-heroku@hartman.me"
    # git pull origin master
}

remove_symlinks() {
    rm -f media
    rm -f database
}

pull_origin() {
    git pull origin master
}

#######################################
# Delete media symlink and move the
# media folder to the parent directory.
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
#######################################
move_media() {
    rm -f /app/media
    mv /app/.heroku-media/media /app/
}

#######################################
# Delete database symlink and move the
# database folder to the parent
# directory.
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
#######################################
move_database() {
    rm -f /app/database
    mv /app/.heroku-media/database /app/
}

#######################################
# Move the .gitignore file to the
# parent directory.
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
#######################################
move_ignore() {
    mv /app/.heroku-media/.gitignore /app/
}

# Run the application thread.
echo "Setting up Git repo."
git_setup
# echo "Moving media folder around."
# move_media
# echo "Moving the database folder."
# move_database
# echo "Moving the .gitignore file."
# move_ignore
echo "Removing original symlink folders."
remove_symlinks
echo "Pulling origina source code."
pull_origin
exit 0
