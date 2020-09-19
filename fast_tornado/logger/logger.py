"""
description: this module provides the class ``Logger``.
"""

import sys
import textwrap
import logging

from fast_tornado.constants import LOGGER

class Logger(logging.Logger):
    """
    description: this is the logger of fast_tornado.
    """

    def __init__(self, name=LOGGER.NAME, **kwargs):
        super().__init__(name)
        self.name = name
        self.level = kwargs.get('level', LOGGER.LEVEL)

        self.__file_path = kwargs.get('file_path', LOGGER.FILE_PATH)
        self.__title_format = kwargs.get('title_format', LOGGER.TITLE_FORMAT)
        self.__format = self.__title_format + '\n' + '%(message)s'
        self.__indent = kwargs.get('indent', LOGGER.INDENT)

        self.__initialize_stream_handler()

    @property
    def file_path(self):
        """
        description: this function is used to get the private member __file_path.
        """
        return self.__file_path

    @property
    def format(self):
        """
        description: this function is used to get the private member __format.
        """
        return self.__format

    @property
    def title_format(self):
        """
        description: this function is used to get the private member __title_format.
        """
        return self.__title_format

    def __initialize_stream_handler(self):
        handler = StreamHandler(stream=sys.stdout, indent=self.__indent)
        handler.setLevel(self.level)
        handler.setFormatter(logging.Formatter(self.__format))
        self.addHandler(handler)

class StreamHandler(logging.StreamHandler):
    """
    description: this class is the subclass of ``logging.StreamHandler``.
    """
    def __init__(self, indent, *args, **kwargs):
        """
        description: override the ``__init__`` function to add an argument ``indent``.
        """
        super().__init__(*args, **kwargs)
        self.__indent = indent

    def emit(self, record):
        """
        description: override the ``emit`` function to add indent in front of ``record.msg``.
        """
        record.msg = textwrap.indent(record.msg, self.__indent * ' ')
        super().emit(record)
