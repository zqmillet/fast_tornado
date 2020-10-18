"""
description: this module provides the exceptions of fast_tornado.
"""

from .base import FastTornadoBaseException

from .match_schema import SchemaException
from .match_schema import TypeMismatchException
from .match_schema import InitializeLambdaExpressionException
from .match_schema import AssertionException
from .match_schema import CannotFindPropertyException
from .match_schema import EnumerationException
from .match_schema import InvalidPropertyException
from .match_schema import DependenciesException
from .match_schema import RegexPatternException
from .match_schema import NonstringTypeHasPatternException
from .match_schema import ExceedMaximumException
from .match_schema import ExceedMinimumException
from .match_schema import LengthRangeException
from .match_schema import MultipleOfException

from .system import CannotFindFileOrDirectoryException
from .system import InvalidArgumentsException
from .system import InvalidYamlException
