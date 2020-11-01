"""
description: this module provides the function generate_request_handler.
"""

import types
import tornado

from fast_tornado.functions import load_yaml
from fast_tornado.match_schema import check_schema

from fast_tornado.exceptions import CannotFindDocumentException
from fast_tornado.exceptions import TypeMismatchException
from fast_tornado.exceptions import InvalidYamlException
from fast_tornado.constants import DOCUMENT_SCHEMA

def generate_request_handler(function):
    """
    description: this function is used to wrap a function to a request handler.
    """
    if not isinstance(function, types.FunctionType):
        raise TypeMismatchException(
            data=function,
            expected_types=[types.FunctionType],
            name='function'
        )

    if function.__doc__ is None:
        raise CannotFindDocumentException(function)

    document = load_yaml(content=function.__doc__)

    check_schema(
        schema=DOCUMENT_SCHEMA,
        data=document,
        name='{name}.__doc__'.format(name='.'.join([function.__module__, function.__name__]))
    )

    class RequestHandler(tornado.web.RequestHandler):
        pass
