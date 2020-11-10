import pytest
import tornado.web

from fast_tornado.server import generate_request_handler

def function(x):
    """
    description: this is description.
    api_path: /test
    methods: [get]
    arguments:
        - name: x
          type: int
          from: query
    return:
        type: int
        description: this is return.
    """
    return x


@pytest.fixture(scope='function', name='application')
def __application():
    request_handler = generate_request_handler(function)
    application = tornado.web.Application(
        [
            ('/test', request_handler)
        ]
    )
    application.listen(8000)
    return application
    
