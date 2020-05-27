#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Application script.

This runs a Flask server which replaces the PHP Webhook functionality.
"""
from flask import Flask, request, json

import log
from db import Db
from git import git_commit
from mail import send_api
from settings import MAIL_ADMIN_FROM_ADDRESS
from utility import Utility


app = Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    utl = Utility()
    db = Db()
    admin_email = MAIL_ADMIN_FROM_ADDRESS
    details = json.loads(request.data)

    # if details['code'] != 405:
    p_event = details['event']
    p_name = details['payload']['item_name']
    p_url = details['payload']['item_url']
    p_date = details['payload']['created_at']

    try:
        """Insert into the database."""
        ins = db.insert_payload(p_event, p_name, p_url, p_date)
        message = {'id': ins, 'item_name': p_name, 'item_url': p_url}
        payload = utl.json_message('success', 200, message)
        log.doc('info', f"id: {ins} -> {p_name} ({p_url}) inserted into db.")
    except Exception as e:
        log.doc('except', f"Error inserting {p_name} into db: {e}")
        send_api(admin_email, 'Webhook DB insert exception', e)
    else:
        try:
            """Send mail with confirmation of db insert."""
            subject = p_name + ' inserted into DB'
            content = 'Inserted ' + p_name + ' (' + p_url + ')'
            send_api(admin_email, subject, content)
            log.doc('info', f"Sent email with subject {subject} to admin.")
        except Exception as e:
            log.doc('except', f"Error sending {subject} email: {e}")
            send_api(admin_email, 'Webhook email/git exception', e)
            raise e
        else:
            """Commit changes to the git repo."""
            log.doc('info', f"Committing changes to GitHub repo.")
            git_commit()
        finally:
            return payload
