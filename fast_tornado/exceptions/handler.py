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

class CannotFindArgumentSchemaException(FastTornadoBaseException):
    """
    description: if some argument schema are missing, raise this exception.
    """
    def __init__(self, missing_argument_names, function):
        super().__init__(
            "cannot find schema of arguments {arguments} in {function}.__doc__['arguments']".format(
                arguments=', '.join(missing_argument_names),
                function='.'.join([function.__module__, function.__name__])
            )
        )

class UnknownArgumentSchemaException(FastTornadoBaseException):
    """
    description: |
        if there are some argument schema, which do not in function signature,
        raise this exception.
    """
    def __init__(self, unknown_argument_names, function):
        super().__init__(
            "there are unknown arguments {arguments} in {function}.__doc__['arguments']".format(
                arguments=', '.join(unknown_argument_names),
                function='.'.join([function.__module__, function.__name__])
            )
        )
