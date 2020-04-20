#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
AMQP Server module.

A module running an AMQP stream server to accept messages and callbacks from
the PHP and Python apps.
"""
import os
import pika
from urllib.parse import urlparse

# Parse CLOUDAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel()

channel.queue_declare(queue='python_queue')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(
    queue='python_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
