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
              error, critical, or exception.
    :type  t: string
    :param m: Log message text.
    :type  m: string

    :returns: Log file with message.
    :rtype:   mixed
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.NOTSET,
        format='[🕒 %(asctime)s] %(name)s %(levelname)s: %(message)s',
        filename='./logs/app.log'
    )

    if "critical" is t:
        data = logger.critical(m)
    elif "error" is t:
        data = logger.error(m)
    elif "warning" is t:
        data = logger.warning(m)
    elif "debug" is t:
        data = logger.debug(m)
    elif "except" is t:
        data = logger.exception(m)
    else:
        data = logger.info(m)

    return data
