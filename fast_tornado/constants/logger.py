"""
description: this module provides constants about logger.
"""

import logging

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

TITLE_FORMAT = '[%(asctime)s][%(name)s][%(levelname)-8s][%(filename)s:%(lineno)d]'
MESSAGE_FORMAT = '%(message)s'
SEPARATOR = '\n'
NAME = 'fast_tornado'
FILE_PATH = None
LEVEL = DEBUG
INDENT = 2
