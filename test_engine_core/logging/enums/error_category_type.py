from enum import Enum


class ErrorCategory(Enum):
    """
    The ErrorCategory enum class specifies the different Error Category
    """

    UNSUPPORTED_DATA = 1
    UNSUPPORTED_MODEL = 2
    INVALID_ARGUMENT = 3
    TESTING_FAULT = 4
    SYSTEM_ERROR = 5
