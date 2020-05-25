#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Logging.

Script to log items to a log file.
"""
import logging


def doc(t, m):
    """
    Document a log entry to the log file.

    :param t: Type of log entry to record. Can be one of info, debug, warn,
              error, critical, exception or general.
    :type  t: string
    :param m: Log message text.
    :type  m: string

    :returns: Log file with message.
    :rtype:   mixed
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.NOTSET,
        format='🕒 %(asctime)s :~$ %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='./logs/app.log'
    )

    if "critical" is t:
        data = logger.critical(f"‼️ {m}")
    elif "error" is t:
        data = logger.error(f"🔴 {m}")
    elif "warning" is t:
        data = logger.warning(f"🟠 {m}")
    elif "debug" is t:
        data = logger.debug(f"🐛 {m}")
    elif "except" is t:
        data = logger.exception(f"❌ {m}")
    elif "general" is t:
        data = logger.info(f"{m}")
    else:
        data = logger.info(f"🟢 {m}")

    return data


def tail(m):
    """
    Document a log entry to the log file.

    :param m: Log message text.
    :type  m: string

    :returns: Log file with message.
    :rtype:   mixed
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.NOTSET,
        format='%(message)s',
        filename='./logs/app.log'
    )

    return logger.info(m)
