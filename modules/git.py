#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Git module.

A module to store uploaded media and edited SQLite databases to GitHub.
"""
from utility import Utility


def commit_db():
    utl = Utility()

    pull = ['git', 'pull', 'origin', 'master']
    utl.sub_process(pull)

    add = ['git', 'add', 'database', 'logs']
    process_add = utl.sub_process(add)

    message = str(':robot: commit from :snake: code.')
    commit = ['git', 'commit', '-am', message]
    process_com = utl.sub_process(commit)

    push = ['git', 'push', '-u', 'origin', 'master']
    process_psh = utl.sub_process(push)

    return process_add, process_com, process_psh
