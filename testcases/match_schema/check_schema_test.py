"""
description: this module contains the testcases about check_schema.
"""

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
def test_int_type(schema, data, exception):
    """
    description: test type mismatch.
    """
    with pytest.raises(TypeMismatchException) as execution_information:
        check_schema(schema, data)

    assert str(execution_information.value) == exception
