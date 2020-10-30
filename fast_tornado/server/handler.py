"""
description: this module provides the function generate_request_handler.
"""

import types

from fast_tornado.exceptions import CannotFindDocumentException
from fast_tornado.exceptions import TypeMismatchException

def generate_request_handler(function):
    """
    description: this function is used to wrap a function to a request handler.
    """
    if not isinstance(function, types.FunctionType):
        raise TypeMismatchException(
            data=function,
            expected_types=[types.FunctionType],
            name='function'
        )

    if function.__doc__ is None:
        raise CannotFindDocumentException(function)
