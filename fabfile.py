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
    push_heroku()


def commit(message):
    """
    $ fab commit::"Message in quotes."
    """
    local('git commit -am "%s"' % message)
    push_github()


def push_github():
    result = local('git push origin master')
    return result.return_code


def push_heroku():
    result = local('git push heroku master')
    return result.return_code


def fetch_local():
    result = local('./bin/fetch')
    return result.return_code


def deploy():
    exec()
    test()


"""Heroku Specific Methods."""
def fetch():
    result = local('heroku run /app/bin/fetch -a cloudapp-webhooks')
    return result.return_code


def ps():
    result = local('heroku ps -a cloudapp-webhooks')
    return result.return_code



def exec():
    result = local('heroku ps:exec -a cloudapp-webhooks')
    return result.return_code


def tail_worker():
    result = local('heroku logs --tail --ps worker -a cloudapp-webhooks')
    return result.return_code


def tail():
    result = local('heroku logs --tail -a cloudapp-webhooks')
    return result.return_code


def test():
    code_dir = '/app/'
    with cd(code_dir):
        run("ls -lha")
