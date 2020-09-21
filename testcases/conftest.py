import pytest
import shutil
import essential_generators

def pytest_configure():
    pytest.text_generator = essential_generators.DocumentGenerator()

@pytest.fixture(scope='session', name='terminal_width')
def __terminal_width():
    return shutil.get_terminal_size().columns
