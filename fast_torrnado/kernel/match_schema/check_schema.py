"""
description: this module provides the function check_schema.
"""

import yaml

from fast_torrnado.kernel.exceptions import TypeMismatchException

TYPES = {
    'int': int,
    'float': float,
    'str': str,
    'dict': dict,
    'list': list,
    'any': object
}

def __initialize_type(schema):
    """
    description: this function is used to initialize types of schema.
    arguments:
        schema:
            type: dict
            description: the schema of data.
    """

    types = schema.get('type', 'any')

    if isinstance(types, list):
        types = tuple([TYPES[item] for item in types])
    elif isinstance(types, str):
        types = (TYPES[types],)

    schema['type'] = types

def check_schema(schema, data, name=None):
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
    __initialize_type(schema)

    expected_types = schema['type']
    if not isinstance(data, expected_types):
        raise TypeMismatchException(data=data, expected_types=expected_types, name='data')
