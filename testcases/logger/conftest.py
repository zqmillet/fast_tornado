import os
import uuid
import logging
import pytest

@pytest.fixture(scope='function', name='file_path')
def __file_path():
    file_path = str(uuid.uuid1()) + '.log'
    if os.path.isfile(file_path):
        os.remove(file_path)

    assert not os.path.isfile(file_path)
    yield file_path

    logging.shutdown() 
    if os.path.isfile(file_path):
        os.remove(file_path)
