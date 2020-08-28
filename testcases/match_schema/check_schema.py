import pytest

from fast_torrnado.kernel.match_schema import check_schema

from fast_torrnado.kernel.exceptions import TypeMismatchException

def test_int_type():
    with pytest.raises(TypeMismatchException) as execution_information:
        check_schema('type: [int, str]', 1.2)

    print(execution_information.value)
