import os
import uuid
import pytest

from fast_tornado.functions import load_yaml
from fast_tornado.exceptions import InvalidYamlException
from fast_tornado.constants import FILE_MODE
from fast_tornado.constants import ENCODE

@pytest.fixture(
    scope='function',
    name='valid_yaml_content_and_data',
    params=[
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
def __valid_yaml_content_and_data(request):
    yield request.param

@pytest.fixture(
    scope='function',
    name='valid_yaml_file_path_and_data',
)
def __valid_yaml_file_path_and_data(valid_yaml_content_and_data):
    content, data = valid_yaml_content_and_data

    file_path = str(uuid.uuid1())

    with open(file_path, mode=FILE_MODE.WRITE, encoding=ENCODE.UTF8) as file:
        file.write(content)

    assert os.path.isfile(file_path)
    yield file_path, data

    if os.path.isfile(file_path):
        os.remove(file_path)

def test_load_yaml_from_string_without_exception(valid_yaml_content_and_data):
    content, data = valid_yaml_content_and_data
    assert load_yaml(content=content) == data

def test_load_yaml_from_file_without_exception(valid_yaml_file_path_and_data):
    file_path, data = valid_yaml_file_path_and_data
    assert load_yaml(file_path=file_path) == data

@pytest.fixture(
    scope='function',
    name='invalid_yaml_content_and_exception_message',
    params=[
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
def __invalid_yaml_content_and_exception_message(request):
    yield request.param

@pytest.fixture(
    scope='function',
    name='invalid_yaml_file_path_and_exception_message',
)
def __invalid_yaml_file_path_and_exception_message(invalid_yaml_content_and_exception_message):
    content, exception_message = invalid_yaml_content_and_exception_message

    file_path = str(uuid.uuid1())

    with open(file_path, mode=FILE_MODE.WRITE, encoding=ENCODE.UTF8) as file:
        file.write(content)

    assert os.path.isfile(file_path)
    yield file_path, exception_message

    if os.path.isfile(file_path):
        os.remove(file_path)

def test_load_yaml_from_string_with_exception(invalid_yaml_content_and_exception_message):
    content, exception_message = invalid_yaml_content_and_exception_message
    with pytest.raises(InvalidYamlException) as execution_infomation:
        load_yaml(content=content)

    assert exception_message in str(execution_infomation.value)

def test_load_yaml_from_file_path_with_exception(invalid_yaml_file_path_and_exception_message):
    file_path, exception_message = invalid_yaml_file_path_and_exception_message
    with pytest.raises(InvalidYamlException) as execution_infomation:
        load_yaml(file_path=file_path)

    assert exception_message in str(execution_infomation.value)
