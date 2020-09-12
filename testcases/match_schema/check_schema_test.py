"""
description: this module contains the testcases about check_schema.
"""

import collections
import pytest

from fast_tornado.kernel.match_schema import check_schema

from fast_tornado.kernel.exceptions import TypeMismatchException
from fast_tornado.kernel.exceptions import AssertionException
from fast_tornado.kernel.exceptions import InitializeLambdaExpressionException
from fast_tornado.kernel.exceptions import CannotFindPropertyException

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

@pytest.mark.parametrize(
    'schema, data', [
        [
            '''
            type: int
            assertion: "lambda x: x > 0"
            ''',
            1
        ],
        [
            '''
            type: [int, float]
            assertion: "lambda x: x > 0"
            ''',
            2.0
        ],
        [
            '''
            type: [int, float, None] 
            assertion: "lambda x: x is None"
            ''',
            None
        ]
    ]
)
def test_assertion_successfully(schema, data):
    check_schema(schema, data)

@pytest.mark.parametrize(
    'schema, data, exception_message', [
        [
            '''
            type: int
            assertion: "lambda x: x > 0"
            ''',
            0,
            "data = 0, cannot pass the assertion 'lambda x: x > 0'"
        ],
        [
            '''
            type: [int, float]
            assertion: "lambda x: x > 0"
            ''',
            -0.1,
            "data = -0.1, cannot pass the assertion 'lambda x: x > 0'"

        ],
        [
            '''
            type: [int, float, None] 
            assertion: "lambda x: x is None"
            ''',
            1,
            "data = 1, cannot pass the assertion 'lambda x: x is None'"
        ]
    ]
)
def test_assertion_failed(schema, data, exception_message):
    with pytest.raises(AssertionException) as execution_information:
        check_schema(schema, data)

    assert str(execution_information.value) == exception_message

@pytest.mark.parametrize(
    'schema, exception_message', [
        [
            '''
            type: int
            assertion: null
            ''',
            "cannot initialize lambda expression from None"
        ],
        [
            '''
            type: int
            assertion: x > 3

            ''',
            "cannot initialize lambda expression from 'x > 3'"
        ],
        [
            '''
            type: int
            assertion: x
            ''',
            "cannot initialize lambda expression from 'x'"
        ]

    ]
)
def test_initialize_lambda_expression_exception(schema, exception_message):
    with pytest.raises(InitializeLambdaExpressionException) as execution_information:
        check_schema(schema, None)
    assert str(execution_information.value) == exception_message

@pytest.mark.parametrize(
    'schema, data', [
        [
            '''
            type: dict
            properties:
                x:
                    type: int
                y:
                    type: int
            ''',
            {'x': 1, 'y': 2}
        ],
        [
            '''
            type: dict
            properties:
                x:
                    type: int
                y:
                    type: int
            ''',
            {'x': 1, 'y': 2, 'z': 3}
        ]
    ]
)
def test_check_properties(schema, data):
    check_schema(schema, data)

@pytest.mark.parametrize(
    'schema, data, exception_message', [
        [
            '''
            type: dict
            properties:
                x:
                    type: int
                y:
                    type: int
            ''',
            {'x': 1},
            "cannot find 'y' in data = {'x': 1}"
        ],
        [
            '''
            type: dict
            properties:
                x:
                    type: int
                y:
                    type: int
            ''',
            {'y': 2, 'z': 3},
            "cannot find 'x' in data = {'y': 2, 'z': 3}"
        ],
        [
            '''
            type: dict
            properties:
                x:
                    type: dict
                    properties:
                        y:
                            type: int
            ''',
            {'x': {}},
            "cannot find 'y' in data['x'] = {}"
        ],
        [
            '''
            type: dict
            properties:
                x:
                    type: dict
                    properties:
                        y:
                            type: dict
                            properties:
                                z:
                                    type: dict
            ''',
            {'x': {'y': {}}},
            "cannot find 'z' in data['x']['y'] = {}"
        ]
    ]
)
def test_check_missing_property(schema, data, exception_message):
    with pytest.raises(CannotFindPropertyException) as execution_information:
        check_schema(schema, data)

    assert str(execution_information.value) == exception_message
