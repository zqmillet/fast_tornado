"""
description: this module provides the exceptions about match_schema.
"""

from .base import FastTornadoBaseException

class SchemaException(FastTornadoBaseException):
    """
    description: this is the base exception of exceptions about match_schema.
    """

class TypeMismatchException(SchemaException):
    """
    description: if the type is wrong, raise this exception.
    """
    def __init__(self, data, expected_types, name):
        super().__init__(
            '{name} = {data}, but its type should be {expected_types}'.format(
                name=name,
                data=repr(data),
                expected_types=', '.join(item.__name__ for item in expected_types)
            )
        )

class AssertionException(SchemaException):
    """
    description: if the data cannot pass the assertion, raise this exception.
    """
    def __init__(self, data, assertion, name):
        super().__init__(
            '{name} = {data}, cannot pass the assertion {assertion}'.format(
                name=name,
                data=repr(data),
                assertion=repr(assertion)
            )
        )


class InitializeLambdaExpressionException(SchemaException):
    """
    description: |
        if there are something wrong while initializing the lambda expression,
        raise this exception.
    """
    def __init__(self, expression):
        super().__init__(
            'cannot initialize lambda expression from {expression}'.format(
                expression=repr(expression)
            )
        )
