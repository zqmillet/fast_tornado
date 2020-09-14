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
