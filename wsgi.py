#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
The main WSGi script.

The entry point for our application. This tells our Gunicorn server how to
interact with the application.
"""
import settings
from application import app


if __name__ == "__main__":
    app.run()
