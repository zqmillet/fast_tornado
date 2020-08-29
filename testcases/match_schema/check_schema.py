"""
description: this module contains the testcases about check_schema.
"""

import pytest

from fast_tornado.kernel.match_schema import check_schema

from fast_tornado.kernel.exceptions import TypeMismatchException

def test_int_type():
    """
    description: test type mismatch.
    """
    with pytest.raises(TypeMismatchException) as execution_information:
        check_schema('type: [int, str]', 1.2)

    print(execution_information.value)
