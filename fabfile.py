#!/usr/bin/env python3
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['local']

"""App Deployments"""
def push():
    local("git push heroku master")


def fetch_local():
    local("./bin/fetch")


def deploy():
    exec()
    test()


"""Heroku Specific Methods."""
def fetch():
    local("heroku run ./bin/fetch -a cloudapp-webhooks")
    # cloudapp-staging


def ps():
    local("heroku ps -a cloudapp-webhooks")


def exec():
    local("heroku ps:exec -a cloudapp-webhooks")


def tail_worker():
    local("heroku logs --tail --ps worker -a cloudapp-webhooks")


def tail():
    local("heroku logs --tail")


def test():
    code_dir = '/app'
    with cd(code_dir):
        run("ls -lha")
