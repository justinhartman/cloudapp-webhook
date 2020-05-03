#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Email module.

A module that provides two email methods. The first is using SendGrid's
Python Library (https://github.com/sendgrid/sendgrid-python) while the other
method sends email using SendInBlue's SMTP service.
"""
import os
import smtplib
from email.mime.text import MIMEText

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import settings


# settings variables
sendgrid_api = os.environ.get('SENDGRID_API_KEY')
sender = settings.MAIL_FROM_NAME
host = settings.SIB_HOST
port = settings.SIB_PORT
username = settings.SIB_USER
password = settings.SIB_PASS
sender = settings.MAIL_FROM_NAME
address = settings.MAIL_FROM_ADDRESS


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
    message = Mail(
        from_email=address,
        to_emails=recipient,
        subject=subject,
        plain_text_content=text)
    try:
        sg = SendGridAPIClient(sendgrid_api)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(e.message)


def send_smtp(recipient, subject, message):
    """
    Sends email using SendInBlue SMTP service.

    :param recipient: Email recipient
    :type  recipient: string
    :param subject:   Email subject
    :type  subject:   string
    :param message:   Plain text message
    :type  message:   string

    :returns: True|Exception
    :rtype:   boolean|mixed
    """
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = address
    msg['To'] = recipient

    with smtplib.SMTP(host, port) as smtp:
        try:
            smtp.login(username, 'password')
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            smtp.quit()
            return bool(smtp)
        except Exception as e:
            print(e)
