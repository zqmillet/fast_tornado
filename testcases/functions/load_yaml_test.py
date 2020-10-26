import os
import pytest

from fast_tornado.functions import load_yaml
from fast_tornado.exceptions import InvalidYamlException

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

@pytest.mark.parametrize(
    'content, exception_message', [
        [
            '''
            a:
            b
            ''',
            'while scanning a simple key'
        ],
        [
            '''
            a: 1
              b: 2
            ''',
            'mapping values are not allowed here'
        ]
    ]
)
def test_load_yaml_from_string_with_exception(content, exception_message):
    with pytest.raises(InvalidYamlException) as execution_infomation:
        load_yaml(content=content)

    assert exception_message in str(execution_infomation.value)
