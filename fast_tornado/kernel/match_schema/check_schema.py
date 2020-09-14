"""
description: this module provides the function check_schema.
"""

import importlib
import yaml

from fast_tornado.kernel.exceptions import TypeMismatchException
from fast_tornado.kernel.exceptions import InitializeLambdaExpressionException
from fast_tornado.kernel.exceptions import AssertionException
from fast_tornado.kernel.exceptions import CannotFindPropertyException
from fast_tornado.kernel.exceptions import EnumerationException
from fast_tornado.kernel.exceptions import InvalidPropertyException
from fast_tornado.kernel.exceptions import DependenciesException

TYPES = {
    'int': int,
    'float': float,
    'str': str,
    'dict': dict,
    'set': set,
    'list': list,
    'any': object,
    'None': type(None)
}


def __load_type(type_string):
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
        types = tuple([__load_type(item) for item in types])
    elif isinstance(types, str):
        types = (__load_type(types),)

    schema['type'] = types

def __initialize_assertion(schema):
    if 'assertion' not in schema:
        return

    try:
        schema['_assertion'] = __get_lambda_expression(schema['assertion'])
    except InitializeLambdaExpressionException as exception:
        raise exception

def __get_lambda_expression(expression):
    try:
        lambda_expression = eval(expression) # pylint: disable = eval-used
    except Exception:
        raise InitializeLambdaExpressionException(expression) from None
    else:
        return lambda_expression

def __check_type(data, schema, name):
    expected_types = schema['type']
    if not isinstance(data, expected_types):
        raise TypeMismatchException(data=data, expected_types=expected_types, name=name)

def __check_assertion(data, schema, name):
    if '_assertion' not in schema:
        return

    if schema['_assertion'](data):
        return

    raise AssertionException(data=data, assertion=schema['assertion'], name=name)

def __check_properties(data, schema, name):
    if 'properties' not in schema:
        return

    for property_name, property_schema in schema['properties'].items():
        required = property_schema.get('required', True)

        if property_name not in data and required:
            raise CannotFindPropertyException(
                data=data,
                property_name=property_name,
                name=name
            )

        if property_name not in data: 
            continue

        dependencies = property_schema.get('dependencies', list())
        for dependency in dependencies:
            if dependency in data:
                continue

            raise DependenciesException(
                data=data,
                name=name,
                property_name=property_name,
                nonexistent_dependencies=sorted(set(dependencies) - data.keys())
            )

        __check_schema(
            schema=property_schema,
            data=data[property_name],
            name='{name}[{property_name}]'.format(name=name, property_name=repr(property_name))
        )

    additional_properities = sorted(set(data) - schema['properties'].keys())
    if not schema.get('additional_properities', True) and additional_properities:
        raise InvalidPropertyException(
            data=data,
            property_names=additional_properities,
            name=name
        )

def __check_items(data, schema, name):
    if 'items' not in schema:
        return

    for index, item in enumerate(data):
        __check_schema(
            data=item,
            schema=schema['items'],
            name='{name}[{index}]'.format(name=name, index=repr(index))
        )

def __check_enumeration(data, schema, name):
    if 'enumeration' not in schema:
        return

    if data in schema['enumeration']:
        return

    raise EnumerationException(
        data=data,
        enumeration=schema['enumeration'],
        name=name
    )

def __check_schema(schema, data, name='data'):
    __initialize_types(schema)
    __initialize_assertion(schema)

    __check_type(data, schema, name)
    __check_assertion(data, schema, name)
    __check_properties(data, schema, name)
    __check_items(data, schema, name)
    __check_enumeration(data, schema, name)

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
    __check_schema(schema, data, name)
