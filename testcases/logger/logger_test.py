import pytest
import logging

from fast_tornado.logger import Logger
from fast_tornado.constants import LOGGER

@pytest.mark.parametrize('name', ['logger', 'fast_tornado'])
@pytest.mark.parametrize('file_path', [None, './fast_tornado.log'])
@pytest.mark.parametrize('title_format', ['%(message)s', '%(asctime)-15s'])
@pytest.mark.parametrize('level', [logging.DEBUG, logging.CRITICAL])
def test_logger_properties(name, file_path, title_format, level):
    logger = Logger(name, file_path=file_path, title_format=title_format, level=level)
    assert logger.name == name
    assert logger.file_path == file_path
    assert logger.title_format == title_format
    assert logger.level == level

    logger = Logger(name, title_format=title_format, level=level)
    assert logger.name == name
    assert logger.file_path is LOGGER.FILE_PATH
    assert logger.title_format == title_format
    assert logger.level == level

    logger = Logger(name, level=level)
    assert logger.name == name
    assert logger.file_path is LOGGER.FILE_PATH
    assert logger.title_format == LOGGER.TITLE_FORMAT
    assert logger.level == level

    logger = Logger(name)
    assert logger.name == name
    assert logger.file_path is LOGGER.FILE_PATH
    assert logger.title_format == LOGGER.TITLE_FORMAT
    assert logger.level == LOGGER.DEBUG

    logger = Logger()
    assert logger.name == LOGGER.NAME
    assert logger.file_path is LOGGER.FILE_PATH
    assert logger.title_format == LOGGER.TITLE_FORMAT
    assert logger.level == LOGGER.DEBUG

@pytest.mark.parametrize('name', ['logger', 'fast_tornado'])
def test_stream_handler(name, capsys):
    logger = Logger(name, indent=2)
    logger.info('1234\n12343')
    logger.warning('1234')
    logger.critical('1234')
    output, error = capsys.readouterr()
    assert error == ''
    print(output)
