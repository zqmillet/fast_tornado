from .base import FastTornadoBaseException

class CannotFindFileOrDirectoryException(FastTornadoBaseException):
    """
    description: if there is no file or directory, raise this exception.
    """
    def __init__(self, path):
        super().__init__('cannot find the file or directory {path}'.format(path=repr(path)))

class InvalidArgumentsException(FastTornadoBaseException):
    """
    description: if the arguments are invalid, raise this exception.
    """
    def __init__(self, function_name, message):
        super().__init__(
            'the arguments of function {function_name} is invalid, {message}'.format(
                function_name=function_name,
                message=message
            )
        )

class InvalidYamlException(FastTornadoBaseException):
    """
    description: if the yaml is invalid, raise this exception.
    """
    def __init__(self, exception):
        super().__init__(exception)
