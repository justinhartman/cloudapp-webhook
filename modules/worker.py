#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
AMQP Worker module.

A module running an AMQP stream server to accept messages and callbacks from
the PHP and Python apps.
"""
import os
from time import sleep
from urllib.parse import urlparse

import pika


def connection():
    """
    CloudAMQP connection.

    :returns: AMQP connection
    :rtype:   object
    """
    url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
    url = urlparse(url_str)
    params = pika.ConnectionParameters(host=url.hostname,
                                       virtual_host=url.path[1:],
                                       credentials=pika.PlainCredentials(
                                        url.username, url.password))

    connection = pika.BlockingConnection(params)

    return connection


def worker(conn, exch, type, php, python):
    """
    AMQP worker method to connect to queues and listen to and send responses.

    :param conn:   The CloudAMQP connection.
    :type  conn:   object
    :param exch:   The exchange.
    :type  exch:   string
    :param type:   The exchange type one of direct, fanout, headers, or topic.
    :type  type:   string
    :param php:    The name of the PHP queue.
    :type  php:    string
    :param python: The name of the Python queue.
    :type  python: string

    :returns: Channel listening for messages.
    :rtype:   object
    """
    channel = conn.channel()
    channel.exchange_declare(exchange=exch, exchange_type=type, durable=True)
    channel.queue_bind(exchange=exch, queue=php)
    channel.queue_bind(exchange=exch, queue=python)

    # Consume queue.
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=php, on_message_callback=php_callback)
    channel.basic_consume(queue=python, on_message_callback=python_callback)

    # Start consuming both queues.
    # channel.start_consuming()

    print(' 🟢  Waiting for messages. To exit press CTRL+C')

    return channel


def php_callback(ch, method, properties, body):
    """
    PHP method callback.

    :param ch:         Channel response ACK.
    :type  ch:         object
    :param method:     The method object.
    :type  method:     object
    :param properties: Channel properties
    :type  properties: object
    :param body:       Message body.
    :type  body:       string
    """
    print(" ✅  Received PHP Message: %r" % body)
    sleep(5)
    print(" ✅  Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def python_callback(ch, method, properties, body):
    """
    PHP method callback.

    :param ch:         Channel response ACK.
    :type  ch:         object
    :param method:     The method object.
    :type  method:     object
    :param properties: Channel properties
    :type  properties: object
    :param body:       Message body.
    :type  body:       string
    """
    print(" ✅  Received Python Message: %r" % body)
    sleep(5)
    print(" ✅  Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


"""Create connection and setup variables for the worker."""
conn = connection()
exchange = 'app.webhook'
exchange_type = 'direct'
queue_one = 'php'
queue_two = 'python'

"""Run the worker method."""
worker(conn, exchange, exchange_type, queue_one, queue_two).start_consuming()
