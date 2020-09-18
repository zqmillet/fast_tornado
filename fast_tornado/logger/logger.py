"""
description: this module provides the class ``Logger``.
"""

import sys
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
        self.__indent = kwargs.get('indent', 2)

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
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(self.level)
        handler.setFormatter(logging.Formatter(self.__format))
        self.addHandler(handler)
