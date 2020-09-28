"""
description: this module provides the class ``Logger``.
"""

import sys
import logging
import logging.handlers

from fast_tornado.constants import LOGGER
from fast_tornado.constants import ENCODE
from fast_tornado.functions import wrap_text

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
        self.__separator = kwargs.get('separator', LOGGER.SEPARATOR)
        self.__indent = kwargs.get('indent', LOGGER.INDENT)
        self.__format = self.__separator.join(
            [self.__title_format, kwargs.get('message_format', LOGGER.MESSAGE_FORMAT)]
        )

        self.__initialize_stream_handler()
        self.__initialize_file_handler()

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

    def __initialize_file_handler(self):
        if not self.__file_path:
            return

        handler = logging.handlers.RotatingFileHandler(self.__file_path, encoding=ENCODE.UTF8)
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
        record.msg = wrap_text(record.msg, indent=self.__indent)
        super().emit(record)
