"""
description: this module provides the exceptions about generate_request_handler.
"""

from .base import FastTornadoBaseException

class CannotFindDocumentException(FastTornadoBaseException):
    """
    description: if the function has no docstring, raise this exception.
    """
    def __init__(self, function):
        super().__init__(
            'cannot find docstring in {function_name}'.format(
                function_name='.'.join([function.__module__, function.__name__])
            )
        )
