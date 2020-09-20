import pytest
import random
import shutil
import essential_generators

from fast_tornado.functions import wrap_text

generator = essential_generators.DocumentGenerator()

@pytest.fixture(scope='session', name='terminal_width')
def __terminal_width():
    return shutil.get_terminal_size().columns

@pytest.mark.parametrize('text', [generator.paragraph() for _ in range(20)])
def test_wrap_only(text, terminal_width):
    maximum_length = max(len(line) for line in wrap_text(text).splitlines())
    assert maximum_length <= terminal_width

@pytest.mark.parametrize(
    'text, width', [[generator.paragraph(), random.randint(1, 100)] for _ in range(20)]
)
def test_wrap_only_with_specified_width(text, width):
    maximum_length = max(len(line) for line in wrap_text(text, width=width).splitlines())
    assert maximum_length <= width

@pytest.mark.parametrize(
    'text, indent', [
        [generator.paragraph(), random.randint(0, 10)] for _ in range(20)
    ]
)
def test_wrap_only_with_indent(text, indent, terminal_width):
    maximum_length = max(len(line.lstrip()) for line in wrap_text(text, indent=indent).splitlines())
    assert maximum_length + indent <= terminal_width

@pytest.mark.parametrize(
    'text, indent, width', [
        [generator.paragraph(), random.randint(0, 10), random.randint(11, 100)] for _ in range(40)
    ]
)
def test_wrap_only_with_indent_and_specified_width(text, indent, width):
    maximum_length = max(
        len(line.lstrip()) for line in wrap_text(text, indent=indent, width=width).splitlines()
    )
    assert maximum_length + indent <= width

@pytest.mark.parametrize('text', [generator.paragraph() for _ in range(20)])
def test_not_wrap(text):
    assert text == wrap_text(text, wrap=False)

@pytest.mark.parametrize('text, width', [[generator.paragraph(), random.randint(1, 10)] for _ in range(20)])
def test_not_wrap_with_width(text, width):
    assert text == wrap_text(text, wrap=False)
