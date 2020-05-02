#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
The main application script.

This runs a Flask server.
"""
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # return do_the_login()
        return 'Returning POST...'
    else:
        # return show_the_login_form()
        return 'Returning GET...'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath /%s' % escape(subpath)
