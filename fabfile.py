#!/usr/bin/env python3
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['local']


"""App Deployments"""
def build(message):
    """
    $ fab build::"Message in quotes."
    """
    local('git commit -am "%s"' % message)
    push_heroku


def commit(message):
    """
    $ fab commit::"Message in quotes."
    """
    local('git commit -am "%s"' % message)
    push_github


def push_github():
    local("git push origin master")


def push_heroku():
    local("git push heroku master")


def fetch_local():
    local("./bin/fetch")


def deploy():
    exec()
    test()


"""Heroku Specific Methods."""
def fetch():
    local("heroku run /app/bin/fetch -a cloudapp-webhooks")
    # cloudapp-staging


def ps():
    local("heroku ps -a cloudapp-webhooks")


def exec():
    local("heroku ps:exec -a cloudapp-webhooks")


def tail_worker():
    local("heroku logs --tail --ps worker -a cloudapp-webhooks")


def tail():
    local("heroku logs --tail -a cloudapp-webhooks")


def test():
    code_dir = '/app/'
    with cd(code_dir):
        run("ls -lha")
