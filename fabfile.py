#!/usr/bin/env python3
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['local']


"""
App Deployments
"""


def build(message):
    """
    $ fab build::"Message in quotes."
    """
    local('/usr/local/bin/git commit -am "%s"' % message)
    push_heroku()


def commit(message):
    """
    $ fab commit::"Message in quotes."
    """
    local('/usr/local/bin/git commit -am "%s"' % message)
    push_github()


def push_github():
    r = local('/usr/local/bin/git push origin master')
    return r.return_code


def push_heroku():
    r = local('/usr/local/bin/git push heroku master')
    return r.return_code


def fetch_local():
    r = local('./bin/fetch')
    return r.return_code


def deploy():
    exec()
    test()


"""
Heroku Specific Methods.
"""


def fetch():
    c = '/usr/local/bin/heroku run /app/bin/fetch -a cloudapp-webhooks'
    r = local(c)
    return r.return_code


def ps():
    r = local('/usr/local/bin/heroku ps -a cloudapp-webhooks')
    return r.return_code


def exec():
    r = local('/usr/local/bin/heroku ps:exec -a cloudapp-webhooks')
    return r.return_code


def exec_staging():
    r = local('/usr/local/bin/heroku ps:exec -a cloudapp-staging')
    return r.return_code


def tail_worker():
    c = '/usr/local/bin/heroku logs --tail --ps worker -a cloudapp-webhooks'
    r = local(c)
    return r.return_code


def tail():
    r = local('/usr/local/bin/heroku logs --tail -a cloudapp-webhooks')
    return r.return_code


def tail_staging():
    r = local('/usr/local/bin/heroku logs --tail -a cloudapp-staging')
    return r.return_code


def test():
    code_dir = '/app/'
    with cd(code_dir):
        run("ls -lha")


def remote():
    c = '/usr/local/bin/heroku ps:exec -a cloudapp-webhooks'
    with local(c):
        run('ls -lha')
