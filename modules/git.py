#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Git module.

A module to store uploaded media and edited SQLite databases to GitLab.
"""
import subprocess
from utility import Utility


def commit_db():
    add = ['git', 'add', 'database/database.sqlite']
    process_add = Utility.sub_process(add)

    message = str('Automated Commit: Updated database.')
    commit = ['git', 'commit', '-am', message]
    process_com = Utility.sub_process(commit)

    push = ['git', 'push', '-u', 'origin', 'master']
    process_psh = Utility.sub_process(push)

    return process_add, process_com, process_psh
