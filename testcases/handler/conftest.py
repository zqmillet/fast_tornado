import pytest
import asyncio
import threading
import tornado.web
import tornado.ioloop

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

def get_application(function, api_path, port):
    request_handler = generate_request_handler(function)
    application = tornado.web.Application(
        [
            (api_path, request_handler)
        ]
    )
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

@pytest.fixture(scope='function', name='application')
def __application():
    from tornado.platform.asyncio import AnyThreadEventLoopPolicy
    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

    thread = threading.Thread(target=get_application, args=(function, '/test', 8000))
    thread.daemon = True
    thread.start()
    yield {
        'api_path': '/test',
        'port': '8000'
    }
