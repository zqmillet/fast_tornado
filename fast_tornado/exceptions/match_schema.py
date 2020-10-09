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

class CannotFindPropertyException(SchemaException):
    """
    description: if there is no specified property, raise this exception.
    """
    def __init__(self, data, property_name, name):
        super().__init__(
            'cannot find \'{property_name}\' in {name} = {data}'.format(
                property_name=property_name,
                name=name,
                data=repr(data)
            )
        )

class EnumerationException(SchemaException):
    """
    description: if the data not in the enumeration, raise this exception.
    """
    def __init__(self, data, enumeration, name):
        super().__init__(
            '{name} = {data}, does not in enumeration {enumeration}'.format(
                name=name,
                data=repr(data),
                enumeration=repr(enumeration)
            )
        )

class InvalidPropertyException(SchemaException):
    """
    description: |
        if there is a property in data, and this property is not defined in schema,
        and the additional_properities is False, raise this exception.
    """
    def __init__(self, data, property_names, name):
        super().__init__(
            'property \'{property_names}\' in {name} = {data} is not allowed'.format(
                property_names=', '.join(property_names),
                name=name,
                data=repr(data)
            )
        )

class DependenciesException(SchemaException):
    """
    description: |
        if dependencies of a property do not exist, raise this exception.
    """
    def __init__(self, data, property_name, name, nonexistent_dependencies):
        super().__init__(
            'property \'{property_name}\' depends on {nonexistent_dependencies}, ' \
            'but {nonexistent_dependencies} does not in {name} = {data}'.format(
                property_name=property_name,
                name=name,
                data=repr(data),
                nonexistent_dependencies=', '.join(repr(item) for item in nonexistent_dependencies)
            )
        )

class RegexPatternException(SchemaException):
    """
    description: if the string does not match the pattern, raise this exception.
    """
    def __init__(self, data, pattern, name):
        super().__init__(
            '{name} = {data}, does not match the regex \'{pattern}\''.format(
                name=name,
                data=repr(data),
                pattern=pattern
            )
        )

class NonstringTypeHasPatternException(SchemaException):
    """
    description: |
        if the schema type does not contain str, but it has pattern field, raise this exception.
    """
    def __init__(self, schema):
        super().__init__(
            'non-string schema {schema} should not have pattern field'.format(
                schema=schema
            )
        )

class ExceedMaximumException(SchemaException):
    """
    description: if the data exceeds the maximum, raise this exception.
    """
    def __init__(self, data, maximum, exclusive_maximum, name):
        operator = '<' if exclusive_maximum else '<='
        super().__init__(
            '{name} = {data}, which should {operator} {maximum}'.format(
                name=name,
                data=repr(data),
                operator=operator,
                maximum=maximum
            )
        )

