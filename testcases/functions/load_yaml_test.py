import os
import pytest

from fast_tornado.functions import load_yaml

@pytest.mark.parametrize(
    'content, data', [
        [
            'a',
            'a'
        ],
        [
            'a: 1',
            {'a': 1}
        ],
        [
            'a: "1"',
            {'a': '1'}
        ],
        [
            '[1, 2, 3]',
            [1, 2, 3]
        ],
        [
            '''
            - 1
            - 2
            - 3
            ''',
            [1, 2, 3]
        ]
    ]
)
def test_load_yaml_from_string_without_exception(content, data):
    assert load_yaml(content=content) == data
