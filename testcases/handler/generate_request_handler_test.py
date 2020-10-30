import pytest

from fast_tornado.server import generate_request_handler
from fast_tornado.exceptions import TypeMismatchException
from fast_tornado.exceptions import CannotFindDocumentException

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
