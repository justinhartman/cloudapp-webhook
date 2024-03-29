#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Git module.

A module to store uploaded media and edited SQLite databases to GitHub.
"""
from utility import Utility
import log


utl = Utility()


def git_pull():
    """
    Fetch the latest files from the GitHub media repository.
    """
    log.doc('info', f"Git: pulling latest media repository.")
    pull = ['git', 'pull', '--quiet', 'origin', 'master']
    process = utl.sub_process(pull)

    return process


def git_commit():
    """
    Commit the latest files to the GitHub media repository.
    """
    log.doc('info', f"Git: committing files to GitHub repository.")
    add = ['git', 'add', 'database', 'logs']
    process_add = utl.sub_process(add)

    message = str(':robot: Commit triggered by :snake:')
    commit = ['git', 'commit', '--quiet', '-am', message]
    process_com = utl.sub_process(commit)

    push = ['git', 'push', '--quiet', '-u', 'origin', 'master']
    process_psh = utl.sub_process(push)

    return process_add, process_com, process_psh
