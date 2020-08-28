class SchemaException(BaseException):
    pass

class TypeMismatchException(SchemaException):
    def __init__(self, data, expected_types, name):
        super().__init__(
            '{name} = {data}, but its type should be {expected_types}'.format(
                name=name,
                data=repr(data),
                expected_types=', '.join(item.__name__ for item in expected_types)
            )
        )
