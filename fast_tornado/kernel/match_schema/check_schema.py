"""
description: this module provides the function check_schema.
"""

import importlib
import yaml

from fast_tornado.kernel.exceptions import TypeMismatchException

TYPES = {
    'int': int,
    'float': float,
    'str': str,
    'dict': dict,
    'set': set,
    'list': list,
    'any': object
}


def __initialize_type(type_string):
    if type_string in TYPES:
        return TYPES[type_string]

    package, clazz = type_string.rsplit('.', 1)
    module = importlib.import_module(package)
    return getattr(module, clazz)

def __initialize_types(schema):
    """
    description: this function is used to initialize types of schema.
    arguments:
        schema:
            type: dict
            description: the schema of data.
    """

    types = schema.get('type', 'any')

    if isinstance(types, list):
        types = tuple([__initialize_type(item) for item in types])
    elif isinstance(types, str):
        types = (__initialize_type(types),)

    schema['type'] = types

def check_schema(schema, data, name='data'):
    """
    description: |
        this function is used to check whether does the data match the schema.
        if the data does not match the schema, this function will raise exception.
    arguments:
        schema:
            type: str
            description: the schema of data.
        data:
            type: any
            description: the data.
    """
    schema = yaml.safe_load(schema)
    __initialize_types(schema)

    expected_types = schema['type']
    if not isinstance(data, expected_types):
        raise TypeMismatchException(data=data, expected_types=expected_types, name=name)
