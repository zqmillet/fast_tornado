"""
description: this module contains the testcases about check_schema.
"""

import collections
import pytest

from fast_tornado.match_schema import check_schema

from fast_tornado.exceptions import TypeMismatchException
from fast_tornado.exceptions import AssertionException
from fast_tornado.exceptions import InitializeLambdaExpressionException
from fast_tornado.exceptions import CannotFindPropertyException
from fast_tornado.exceptions import EnumerationException
from fast_tornado.exceptions import InvalidPropertyException
from fast_tornado.exceptions import DependenciesException
from fast_tornado.exceptions import RegexPatternException
from fast_tornado.exceptions import NonstringTypeHasPatternException
from fast_tornado.exceptions import ExceedMaximumException

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
        ['type: null', None],
        ['type: [null]', None],
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
        ['type: None', None],
        ['type: [None]', None],
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
            {'y': 2},
            "cannot find 'x' in data = {'y': 2}"
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


@pytest.mark.parametrize(
    'schema, data, exception_message', [
        [
            '''
            type: list
            items:
                type: int
            ''',
            [1, 2, 3.0],
            'data[2] = 3.0, but its type should be int'
        ],
        [
            '''
            type: list
            items:
                type: dict
            ''',
            [{'x': 1}, []],
            'data[1] = [], but its type should be dict'
        ],
        [
            '''
            type: list
            items:
                type: dict
                properties:
                    x:
                        type: int
            ''',
            [{'x': 1}, {'x': '1'}],
            "data[1]['x'] = '1', but its type should be int"
        ],
        [
            '''
            type: dict
            properties:
                x:
                    type: list
                    items:
                        type: int
            ''',
            {'x': [1, 2, 3.0]},
            "data['x'][2] = 3.0, but its type should be int"
        ],
        [
            '''
            type: list
            items:
                type: list
                items:
                    type: list
                    items:
                        type: int
            ''',
            [[], [[]], [[1, 2, 3.0]], []],
            'data[2][0][2] = 3.0, but its type should be int'
        ]
    ]
)
def test_check_items_with_exception(schema, data, exception_message):
    with pytest.raises(TypeMismatchException) as execution_information:
        check_schema(schema, data)

    assert str(execution_information.value) == exception_message

@pytest.mark.parametrize(
    'schema, data', [
        [
            '''
            type: list
            items:
                type: int
            ''',
            [1, 2, 3]
        ],
        [
            '''
            type: list
            items:
                type: int
            ''',
            []
        ],
        [
            '''
            type: list
            items:
                type: [int, float]
            ''',
            [1, 2, 3.0, 4.4]
        ],
        [
            '''
            type: list
            items:
                type: list
            ''',
            [[], [1], [1, 2, 3]]
        ],
        [
            '''
            type: list
            items:
                type: list
                items:
                    type: int
            ''',
            [[], [1], [1, 2, 3]]
        ],
        [
            '''
            type: list
            items:
                type: list
                items:
                    type: [int, str, float]
            ''',
            [[], [1], [1, 2, 3, '4', 5.1]]
        ]

    ]
)
def test_check_items_without_exception(schema, data):
    check_schema(schema, data)

@pytest.mark.parametrize(
    'schema, data, exception_message', [
        [
            '''
            type: int
            enumeration: [1, 2, 3]
            ''',
            4,
            'data = 4, does not in enumeration [1, 2, 3]'
        ],
        [
            '''
            type: str
            enumeration: [x, y, z]
            ''',
            'w',
            "data = 'w', does not in enumeration ['x', 'y', 'z']"
        ],
        [
            '''
            type: list
            items:
                type: int
                enumeration: [1, 2, 3]
            ''',
            [1, 2, 3, 4, 5],
            'data[3] = 4, does not in enumeration [1, 2, 3]'
        ],
        [
            '''
            type: list
            items:
                type: dict
                properties:
                    x:
                        type: str
                        enumeration: [x, y, z]
            ''',
            [{'x': 'x'}, {'x': 'w'}, {'x': 'y'}],
            "data[1]['x'] = 'w', does not in enumeration ['x', 'y', 'z']"
        ]
    ]
)
def test_enumeration_with_exception(schema, data, exception_message):
    with pytest.raises(EnumerationException) as execution_information:
        check_schema(schema, data)

    assert str(execution_information.value) == exception_message

@pytest.mark.parametrize(
    'schema, data', [
        [
            '''
            type: int
            enumeration: [1, 2, 3]
            ''',
            1
        ],
        [
            '''
            type: list
            items:
                type: [int, str]
                enumeration: [1, 2, 3, x, y, z]
            ''',
            [1, 1, 'x', 'y']
        ],
        [
             '''
            type: list
            items:
                type: [int, str, None]
                enumeration: [1, 2, 3, x, y, z, null]
            ''',
            [1, 1, 'x', None]
        ]
    ]
)
def test_enumeration_without_exception(schema, data):
    check_schema(schema, data)

@pytest.mark.parametrize(
    'schema, data', [
        [
            '''
            type: dict
            properties:
                x:
                    type: int
                    required: false
                y:
                    type: int
            ''',
            {'y': 1}
        ],
        [
            '''
            type: list
            items:
                type: dict
                properties:
                    x:
                        type: int
                        required: false
                    y:
                        type: int
            ''',
            [{'y': 1}, {'x': 1, 'y': 2}, {'y': 3, 'z': 3}]
        ]
    ]
)
def test_required_field_in_properties_without_exception(schema, data):
    check_schema(schema, data)

@pytest.mark.parametrize(
    'schema, data, exception_message', [
        [
            '''
            type: dict
            properties:
                x:
                    type: int
                    required: false
                y:
                    type: int
                    required: true
            ''',
            {},
            "cannot find 'y' in data = {}"
        ],
        [
            '''
            type: list
            items:
                type: dict
                properties:
                    x:
                        type: int
                        required: false
                    y:
                        type: int
                        required: true
            ''',
            [{'z': 1}, {'x': 1, 'y': 2}, {'y': 3, 'z': 3}],
            "cannot find 'y' in data[0] = {'z': 1}"
        ]
    ]
)
def test_required_field_in_properties_with_exception(schema, data, exception_message):
    with pytest.raises(CannotFindPropertyException) as execution_information:
        check_schema(schema, data)

    assert str(execution_information.value) == exception_message

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
            additional_properities: false
            ''',
            {'x': 1, 'y': 2, 'z': 3},
            "property 'z' in data = {data} is not allowed".format(
                data=repr({'x': 1, 'y': 2, 'z': 3})
            )
        ],
        [
            '''
            type: list
            items:
                type: dict
                properties:
                    x:
                        type: int
                        required: false
                    y:
                        type: int
                        required: false
                additional_properities: false
            ''',
            [{}, {'x': 1}, {'z': 3}],
            "property 'z' in data[2] = {'z': 3} is not allowed"
        ]
    ]
)
def test_additional_properties_with_exception(schema, data, exception_message):
    with pytest.raises(InvalidPropertyException) as execution_information:
        check_schema(schema, data)

    assert str(execution_information.value) == exception_message

@pytest.mark.parametrize(
    'schema, data, exception_message', [
        [
            '''
            type: dict
            properties:
                x:
                    type: int
                    dependencies: [y]
                    required: false
                y:
                    type: int
                    dependencies: [x]
                    required: false
            ''',
            {'x': 1},
            "property 'x' depends on 'y', but 'y' does not in data = {'x': 1}"
        ],
        [
            '''
            type: dict
            properties:
                x:
                    type: int
                    dependencies: [y]
                    required: false
                y:
                    type: int
                    dependencies: [x]
                    required: false
            ''',
            {'y': 1},
            "property 'y' depends on 'x', but 'x' does not in data = {'y': 1}"
        ],
        [
            '''
            type: dict
            properties:
                x:
                    type: int
                    required: false
                y:
                    type: int
                    required: false
                z:
                    type: int
                    dependencies: [x, y]
            ''',
            {'z': 1},
            "property 'z' depends on 'x', 'y', but 'x', 'y' does not in data = {'z': 1}"
        ],

    ]
)
def test_dependencies_with_exception(schema, data, exception_message):
    with pytest.raises(DependenciesException) as execution_information:
        check_schema(schema, data) 

    assert str(execution_information.value) == exception_message

@pytest.mark.parametrize(
    'schema', [
        '''
        type: dict
        properties:
            x:
                type: int
                dependencies: [y]
                required: false
            y:
                type: int
                dependencies: [x]
                required: false
        '''
    ]
)
@pytest.mark.parametrize(
    'data', [
        {'x': 1, 'y': 2},
        {},
        {'z': 3},
        {'x': 1, 'y': 2, 'z': 3},
    ]
)
def test_dependencies_without_exception(schema, data):
    check_schema(schema, data) 

@pytest.mark.parametrize(
    'schema, data, exception_message', [
        [
            '''
            type: str
            pattern: \\d+
            ''',
            'abc',
            "data = 'abc', does not match the regex '\\d+'"
        ],
        [
            '''
            type: str
            pattern: "[a-zA-Z]+"
            ''',
            '123',
            "data = '123', does not match the regex '[a-zA-Z]+'"
        ],
        [
            '''
            type: str
            pattern: "[a-zA-Z]{2,3}"
            ''',
            'a',
            "data = 'a', does not match the regex '[a-zA-Z]{2,3}'"
        ]
    ]
)
def test_pattern_with_exception(data, schema, exception_message):
    with pytest.raises(RegexPatternException) as execution_information:
        check_schema(schema, data)

    assert str(execution_information.value) == exception_message

@pytest.mark.parametrize(
    'schema, data', [
        [
            '''
            type: str
            pattern: \\d+
            ''',
            '1234567'
        ],
        [
            '''
            type: str
            pattern: "[a-zA-Z]+"
            ''',
            'abcdefg'
        ],
        [
            '''
            type: str
            pattern: "[a-zA-Z]{2,3}"
            ''',
            'ab'
        ]
    ]
)
def test_pattern_without_exception(data, schema):
    check_schema(schema, data)

@pytest.mark.parametrize(
    'schema', [
        '''
        type: int
        pattern: \\d+
        ''',
        '''
        type: dict
        pattern: \\d+
        ''',
        '''
        type: [dict]
        pattern: \\d+
        ''',
        '''
        type: [dict, float]
        pattern: \\d+
        '''
    ]    
)
def test_non_string_type_with_pattern(schema):
    with pytest.raises(NonstringTypeHasPatternException) as execution_information:
        check_schema(schema, None)

    assert 'non-string schema' in str(execution_information.value)
    assert 'should not have pattern field' in str(execution_information.value)

@pytest.mark.parametrize(
    'schema, data', [
        [
            '''
            type: int
            maximum: 10
            ''',
            0
        ],
        [
            '''
            type: float
            maximum: 10
            ''',
            10.0
        ],
        [
            '''
            type: float
            maximum: 10
            exclusive_maximum: true
            ''',
            9.2
        ],
        [
            '''
            type: float
            maximum: 10
            exclusive_maximum: false
            ''',
            10.0
        ]
    ]
)
def test_maximum_without_exception(data, schema):
    check_schema(schema, data)

@pytest.mark.parametrize(
    'schema, data, exception_message', [
        [
            '''
            type: int
            maximum: 10
            ''',
            11,
            'data = 11, which should <= 10'
        ],
        [
            '''
            type: float
            maximum: 0
            ''',
            1.2,
            'data = 1.2, which should <= 0'
        ],
        [
            '''
            type: int
            maximum: 10
            exclusive_maximum: true
            ''',
            10,
            'data = 10, which should < 10'
        ],
        [
            '''
            type: [int, float]
            maximum: 9
            exclusive_maximum: false
            ''',
            10,
            'data = 10, which should <= 9'
        ]
    ]
)
def test_maximum_with_exception(data, schema, exception_message):
    with pytest.raises(ExceedMaximumException) as execution_information:
        check_schema(schema, data)

    assert str(execution_information.value) == exception_message
