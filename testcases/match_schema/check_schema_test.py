"""
description: this module contains the testcases about check_schema.
"""

import collections
import pytest

from fast_tornado.kernel.match_schema import check_schema

from fast_tornado.kernel.exceptions import TypeMismatchException

@pytest.mark.parametrize(
    'schema, data, exception', [
        [
            'type: [int, str]',
            1.2,
            'data = 1.2, but its type should be int, str'
        ],
        [
            'type: [int]',
            1.2,
            'data = 1.2, but its type should be int'
        ],
        [
            'type: int',
            1.2,
            'data = 1.2, but its type should be int'
        ],
        [
            'type: dict',
            1.2,
            'data = 1.2, but its type should be dict'
        ],
        [
            'type: dict',
            [1, 2, 3],
            'data = [1, 2, 3], but its type should be dict'
        ],
        [
            'type: [dict, int, float, set]',
            [1, 2, 3],
            'data = [1, 2, 3], but its type should be dict, int, float, set'
        ]

    ]
)
def test_type_mismatch(schema, data, exception):
    """
    description: test type mismatch.
    """
    with pytest.raises(TypeMismatchException) as execution_information:
        check_schema(schema, data)

    assert str(execution_information.value) == exception

@pytest.mark.parametrize(
    'schema, data', [
        ['type: int', 1],
        ['type: [int, float]', 1],
        ['type: [int, float]', 1.2],
        ['type: any', 1.2],
        ['type: any', dict()],
        ['type: any', list()],
        ['type: any', Exception()],
        ['type: any', BaseException()],
        ['type: any', type],
        ['type: any', abs],
        ['type: any', isinstance],
        ['type: any', None],
        ['type: any', object],
        ['type: any', object()],
        ['type: [dict, list]', dict()],
        ['type: [dict, list]', [1, 2, 3]],
        ['type: [dict, list]', list()],
        ['type: [dict, list]', {'x': 3, 'y': 1}],
    ]
)
def test_type_match(schema, data):
    """
    description: test type match.
    """
    check_schema(schema, data)

@pytest.mark.parametrize(
    'schema, data', [
        ['type: types.FunctionType', lambda x: x],
        ['type: collections.Counter', collections.Counter()],
        ['type: collections.Counter', collections.Counter(x=1, y=2)],
        ['type: collections.OrderedDict', collections.OrderedDict()],
        ['type: collections.OrderedDict', collections.OrderedDict(x=1, y=2)],
        ['type: [types.FunctionType, int]', lambda x: x],
        ['type: [types.FunctionType, int]', 4],
        ['type: [collections.Counter, dict]', collections.Counter()],
        ['type: [collections.Counter, dict]', {'x': 1}],
        ['type: [collections.Counter]', collections.Counter(x=1, y=2)],
        ['type: [collections.OrderedDict, types.FunctionType]', collections.OrderedDict()],
        ['type: [collections.OrderedDict, types.FunctionType]', lambda x: x + 1],
        ['type: [collections.OrderedDict, types.FunctionType, any]', 1],
        ['type: [collections.OrderedDict, types.FunctionType, any]', dict()],
        ['type: [collections.OrderedDict, types.FunctionType, any]', type],
        ['type: [collections.OrderedDict, types.FunctionType, any]', dict],
    ]
)
def test_complex_type_match(schema, data):
    """
    description: test complex type match.
    """
    check_schema(schema, data)

@pytest.mark.parametrize(
    'schema, data, exception', [
        [
            'type: types.FunctionType',
            1,
            'data = 1, but its type should be function'
        ],
        [
            'type: [types.FunctionType]',
            1,
            'data = 1, but its type should be function'
        ],
        [
            'type: [types.FunctionType, collections.OrderedDict]',
            1,
            'data = 1, but its type should be function, OrderedDict'
        ],
        [
            'type: [types.FunctionType, collections.OrderedDict, dict]',
            1,
            'data = 1, but its type should be function, OrderedDict, dict'
        ],

    ]
)
def test_complex_type_mismatch(schema, data, exception):
    """
    description: test complex type match.
    """
    with pytest.raises(TypeMismatchException) as execution_information:
        check_schema(schema, data)

    assert str(execution_information.value) == exception
