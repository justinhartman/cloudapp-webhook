#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Git module.

A module to store uploaded media and edited SQLite databases to GitLab.
"""
from utility import Utility


def commit_db():
    utl = Utility()
    add = ['git', 'add', '*']
    process_add = utl.sub_process(add)

    message = str('Automated: Python commit.')
    commit = ['git', 'commit', '-m', message]
    process_com = utl.sub_process(commit)

    push = ['git', 'push', '-u', 'origin', 'master']
    process_psh = utl.sub_process(push)

    return process_add, process_com, process_psh
