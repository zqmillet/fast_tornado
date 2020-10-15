"""
description: this module provides the function check_schema.
"""

import re
import math
import importlib
import collections.abc
import yaml

from fast_tornado.exceptions import TypeMismatchException
from fast_tornado.exceptions import InitializeLambdaExpressionException
from fast_tornado.exceptions import AssertionException
from fast_tornado.exceptions import CannotFindPropertyException
from fast_tornado.exceptions import EnumerationException
from fast_tornado.exceptions import InvalidPropertyException
from fast_tornado.exceptions import DependenciesException
from fast_tornado.exceptions import RegexPatternException
from fast_tornado.exceptions import NonstringTypeHasPatternException
from fast_tornado.exceptions import ExceedMaximumException
from fast_tornado.exceptions import ExceedMinimumException
from fast_tornado.exceptions import LengthRangeException
from fast_tornado.exceptions import MultipleOfException

TYPES = {
    'int': int,
    'float': float,
    'str': str,
    'dict': dict,
    'set': set,
    'list': list,
    'tuple': tuple,
    'any': object,
    'None': type(None),
}


def __load_type(type_string):
    type_string = str(type_string)
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
    elif types is None:
        types = (type(None),)
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

def __check_dict_type_items(data, schema, name):
    items_schema = schema.get('items')
    if not isinstance(items_schema, dict):
        return

    for index, item in enumerate(data):
        __check_schema(
            data=item,
            schema=items_schema,
            name='{name}[{index}]'.format(name=name, index=repr(index))
        )

def __check_list_type_items(data, schema, name):
    items_schema = schema.get('items')
    if not isinstance(items_schema, list):
        return

    if not len(items_schema) == len(data):
        raise LengthRangeException(
            name=name,
            data=data,
            maximum_length=len(items_schema),
            minimum_length=len(items_schema)
        ) 

    for index, (item_schema, item) in enumerate(zip(items_schema, data)):
        __check_schema(
            data=item,
            schema=item_schema,
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

def __check_pattern(data, schema, name):
    if 'pattern' not in schema:
        return

    if re.match(pattern=schema['pattern'], string=data) :
        return

    raise RegexPatternException(
        name=name,
        data=data,
        pattern=schema['pattern']
    )

def __check_validation(schema):
    if str not in schema['type'] and 'pattern' in schema:
        raise NonstringTypeHasPatternException(schema=schema)

def __check_maximum(data, schema, name):
    if not 'maximum' in schema:
        return

    maximum = schema['maximum']

    exclusive_maximum = schema.get('exclusive_maximum', False)
    if exclusive_maximum:
        check = lambda x, y: x < y
    else:
        check = lambda x, y: x <= y

    if not check(data, maximum):
        raise ExceedMaximumException(
            name=name,
            exclusive_maximum=exclusive_maximum,
            data=data,
            maximum=maximum
        )

def __check_minimum(data, schema, name):
    if not 'minimum' in schema:
        return

    minimum = schema['minimum']

    exclusive_minimum = schema.get('exclusive_minimum', False)
    if exclusive_minimum:
        check = lambda x, y: x > y
    else:
        check = lambda x, y: x >= y

    if not check(data, minimum):
        raise ExceedMinimumException(
            name=name,
            exclusive_minimum=exclusive_minimum,
            data=data,
            minimum=minimum
        )

def __check_length(data, schema, name):
    if not isinstance(data, collections.abc.Sized):
        return

    minimum_length = schema.get('minimum_length', 0)
    maximum_length = schema.get('maximum_length', math.inf)

    if minimum_length <= len(data) <= maximum_length:
        return

    raise LengthRangeException(
        name=name,
        data=data,
        maximum_length=maximum_length,
        minimum_length=minimum_length
    )

def __check_multiple_of(data, schema, name):
    if not 'multiple_of' in schema:
        return

    multiple_of = schema['multiple_of']
    if not data % multiple_of:
        return

    raise MultipleOfException(
        name=name,
        data=data,
        multiple_of=multiple_of
    )

def __check_schema(schema, data, name='data'):
    __initialize_types(schema)
    __initialize_assertion(schema)
    __check_validation(schema)

    __check_type(data, schema, name)
    __check_assertion(data, schema, name)
    __check_properties(data, schema, name)
    __check_dict_type_items(data, schema, name)
    __check_list_type_items(data, schema, name)
    __check_enumeration(data, schema, name)
    __check_pattern(data, schema, name)
    __check_maximum(data, schema, name)
    __check_minimum(data, schema, name)
    __check_length(data, schema, name)
    __check_multiple_of(data, schema, name)

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
