"""
description: this module provides the function load_yaml.
"""

import os
import yaml

from fast_tornado.constants import FILE_MODE
from fast_tornado.constants import ENCODE

from fast_tornado.exceptions import CannotFindFileOrDirectoryException
from fast_tornado.exceptions import InvalidArgumentsException
from fast_tornado.exceptions import InvalidYamlException

def load_yaml(*, file_path=None, content=None):
    """
    description: this function is used to load yaml from string or file path.
    """
    if (file_path is None and content is None) or (file_path is not None and content is not None):
        raise InvalidArgumentsException(
            function_name='load_yaml',
            message='you must specify the value for argument file_path or content'
        )

    if file_path:
        if not os.path.isfile(file_path):
            raise CannotFindFileOrDirectoryException(path=file_path)

        with open(file_path, FILE_MODE.READ, encoding=ENCODE.UTF8) as file:
            content = file.read()

    try:
        return yaml.safe_load(content)
    except yaml.error.YAMLError as exception:
        raise InvalidYamlException(exception) from None
