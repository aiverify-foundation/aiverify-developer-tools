from enum import Enum


class ErrorOrigin(Enum):
    """
    The ErrorOrigin enum class specifies the different Error origin
    """

    USER_ERROR = 1
    SYSTEM_ERROR = 2
