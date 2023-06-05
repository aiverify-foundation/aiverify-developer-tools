from enum import Enum


class ServiceType(Enum):
    """
    The ServiceType enum class specifies the different service types
    """

    VALIDATE_MODEL = 1
    VALIDATE_DATASET = 2
