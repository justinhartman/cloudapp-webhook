#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Email module.

A module that provides two email methods. The first is using SendGrid's
Python Library (https://github.com/sendgrid/sendgrid-python) while the other
method sends email using SendInBlue's SMTP service.
"""
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import settings


def send_api(recipient, subject, text):
    """
    Send email from SendGrid API.

    :param recipient: Email recipient
    :type  recipient: string
    :param subject:   Email subject
    :type  subject:   string
    :param text:      Plain text message
    :type  text:      string

    :returns: Status|Exception
    :rtype:   mixed
    """
    mailer = Mail(
        from_email=settings.MAIL_FROM_ADDRESS,
        to_emails=recipient,
        subject=subject,
        html_content=text)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(mailer)
        return response.status_code
    except Exception as e:
        print(e)
