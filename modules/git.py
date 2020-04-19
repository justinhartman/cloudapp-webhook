#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Git module.

A module to store uploaded media and edited SQLite databases to GitLab.
"""
from utility import Utility


def commit_db():
    utl = Utility()
    # add = ['git', 'add', 'database/database.sqlite']
    # process_add = utl.sub_process(add)

    message = str('Automated: Python DB and Logs.')
    commit = ['git', 'commit', '-am', message]
    process_com = utl.sub_process(commit)

    push = ['git', 'push', '-u', 'origin', 'master']
    process_psh = utl.sub_process(push)

    # return process_add, process_com, process_psh
    return process_com, process_psh
