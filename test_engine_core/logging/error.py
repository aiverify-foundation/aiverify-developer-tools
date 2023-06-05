from dataclasses import dataclass
from typing import Dict

from test_engine_core.logging.enums.error_category_type import ErrorCategory
from test_engine_core.logging.enums.error_origin_type import ErrorOrigin
from test_engine_core.logging.enums.error_severity_type import ErrorSeverity


@dataclass
class Error:
    """
    The Error dataclass comprises information on the error such as category, code,
    description, severity, origin and component
    """

    category: ErrorCategory
    code: str
    description: str
    severity: ErrorSeverity
    origin: ErrorOrigin
    component: str

    def __init__(
        self,
        category: ErrorCategory,
        code: str,
        description: str,
        severity: ErrorSeverity,
        origin: ErrorOrigin,
        component: str,
    ):
        self.category = category
        self.code = code
        self.description = description
        self.severity = severity
        self.origin = origin
        self.component = component

    def get_dict(self) -> Dict:
        """
        A method to return the dictionary of items of Error

        Returns:
            Dict: A dictionary of required information to be sent back by redis
        """
        return {
            "category": self.category.name,
            "code": self.code,
            "description": self.description,
            "severity": self.severity.name.lower(),
            "origin": self.origin.name,
            "component": self.component,
        }
