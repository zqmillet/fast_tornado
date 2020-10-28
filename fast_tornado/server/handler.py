"""
description: this module provides the function generate_request_handler.
"""

import types
import tornado

from fast_tornado.exceptions import CannotFindDocumentException
from fast_tornado.exceptions import TypeMismatchException

def generate_request_handler(function):
    if not isinstance(function, types.FunctionType):
        raise TypeMismatchException(
            data=function,
            expected_types=[types.FunctionType],
            name='function'
        )

    if function.__doc__ is None:
        raise CannotFindDocumentException(function)
