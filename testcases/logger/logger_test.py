import re
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

@pytest.mark.parametrize(
    'name', ['logger', 'fast_tornado']
)
@pytest.mark.parametrize(
    'level', [LOGGER.DEBUG, LOGGER.INFO, LOGGER.WARNING, LOGGER.ERROR, LOGGER.CRITICAL]
)
@pytest.mark.parametrize(
    'message', [pytest.text_generator.paragraph() for _ in range(3)]
)
@pytest.mark.parametrize(
    'indent', [0, 1, 2, 4]
)
def test_stream_handler(name, level, message, indent, capsys, terminal_width):
    logger = Logger(name, indent=indent, level=level)
    logger.debug(message)
    logger.info(message)
    logger.warning(message)
    logger.error(message)
    logger.critical(message)
    output, error = capsys.readouterr()

    assert not error

    title_pattern = r'\[(?P<time>.+)\]\[(?P<name>.+)\]\[(?P<level>.+)\]\[(?P<file_name>.+):(?P<line_number>.+)\]'
    time_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}'

    for line in output.splitlines():
        result = re.match(pattern=title_pattern, string=line)
        if result:
            group_dictionary = result.groupdict()
            assert re.match(time_pattern, group_dictionary['time'])
            assert group_dictionary['name'] == name
            assert group_dictionary['file_name'] == __file__
            assert logging.getLevelName(group_dictionary['level'].strip()) >= level 
            assert group_dictionary['line_number'].isdigit()
        else:
            prefix = line[:indent]
            message = line[indent:]
            assert prefix == ' ' * indent
            assert not message.startswith(' ')
            assert len(line) <= terminal_width
