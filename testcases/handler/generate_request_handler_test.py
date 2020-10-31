import pytest

from fast_tornado.server import generate_request_handler
from fast_tornado.exceptions import TypeMismatchException
from fast_tornado.exceptions import CannotFindDocumentException
from fast_tornado.exceptions import InvalidYamlException
from fast_tornado.exceptions import SchemaException

@pytest.mark.parametrize(
    'function', [
        '1',
        list(),
        dict(),
        set(),
        1,
        1.1,
        None
    ]
)
def test_type_mismatch_exception(function):
    with pytest.raises(TypeMismatchException) as execution_infomation:
        generate_request_handler(function)

    assert str(execution_infomation.value) == 'function = {function}, but its type should be function'.format(
        function=repr(function)
    )

@pytest.fixture(scope='function', name='function_without_document')
def __function_without_document(request):
    def wrapper():
        pass
    return wrapper

def test_cannot_find_document_exception(function_without_document):
    with pytest.raises(CannotFindDocumentException) as execution_infomation:
        generate_request_handler(function_without_document)

    assert str(execution_infomation.value) == 'cannot find docstring in generate_request_handler_test.wrapper'

@pytest.fixture(
    scope='function',
    name='function_with_invalid_yaml_document',
    params=[
        '''
        a: 1
            b: 2
        ''',
        '''
        a: [1, 2, 3
        ''',
        '''
        [- 1, 2, 3]
        '''
    ]
)
def __function_with_invliad_yaml_document(request):
    def wrapper():
        pass

    wrapper.__doc__ = request.param
    return wrapper 

def test_invalid_yaml_exception(function_with_invalid_yaml_document):
    with pytest.raises(InvalidYamlException) as execution_infomation:
        generate_request_handler(function_with_invalid_yaml_document)

@pytest.fixture(
    scope='function',
    name='function_with_invalid_format_document_and_reason',
    params=[
        [
            '',
            "generate_request_handler_test.wrapper.__doc__ = None, but its type should be dict"
        ],
        [
            '1',
            "generate_request_handler_test.wrapper.__doc__ = 1, but its type should be dict"
        ],
        [
            'description: this is description',
            "cannot find 'methods' in generate_request_handler_test.wrapper.__doc__ = {'description': 'this is description'}"
        ],
        [
            '''
            description: this is description
            methods: [get]
            ''',
            "cannot find 'api_path' in generate_request_handler_test.wrapper.__doc__"
        ],
        [
            '''
            description: this is description
            methods: [get]
            api_path: /test
            return: null
            ''',
            "generate_request_handler_test.wrapper.__doc__['return'] = None, but its type should be dict"
        ],
        [
            '''
            description: this is description
            methods: [get]
            api_path: /test
            return:
                description: this is return
            ''',
            "cannot find 'type' in generate_request_handler_test.wrapper.__doc__['return']"
        ],
        [
            '''
            description: this is description
            methods: [get]
            api_path: /test
            arguments:
            return:
                description: this is return
                type: str
            ''',
            "generate_request_handler_test.wrapper.__doc__['arguments'] = None, but its type should be list"
        ],
        [
            '''
            description: this is description
            methods: [get]
            api_path: /test
            arguments:
                - name: x
                  type: str
            return:
                description: this is return
                type: str
            ''',
            "cannot find 'from' in generate_request_handler_test.wrapper.__doc__['arguments'][0]"
        ],
        [
            '''
            description: this is description
            methods: [get]
            api_path: /test
            arguments:
                - name: x
                  type: str
                  from: haha
            return:
                description: this is return
                type: str
            ''',
            "['arguments'][0]['from'] = 'haha', does not in enumeration ['query', 'path', 'body', 'header', 'entire_body']"
        ]
    ]
)
def __function_with_invliad_format_document_and_reason(request):
    def wrapper():
        pass

    wrapper.__doc__, reason = request.param
    return wrapper, reason

def test_invalid_format_exception(function_with_invalid_format_document_and_reason):
    function, reason = function_with_invalid_format_document_and_reason
    with pytest.raises(SchemaException) as execution_infomation:
        generate_request_handler(function)

    print(execution_infomation.value)
    assert reason in str(execution_infomation.value)
