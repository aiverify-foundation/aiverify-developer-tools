import json
from pathlib import Path
from typing import List

from test_engine_core.logging.enums.error_category_type import ErrorCategory
from test_engine_core.logging.enums.error_origin_type import ErrorOrigin
from test_engine_core.logging.enums.error_severity_type import ErrorSeverity
from test_engine_core.logging.error import Error
from test_engine_core.utils.json_utils import scan_for_single_quotes


class ErrorManager:
    """
    The ErrorManager class comprises methods to create new error managers and store errors created while in operation
    """

    def __init__(self):
        """
        Initialisation of ErrorManager
        """
        self._name: str = "error_file"
        self._filepath: str = ""
        self._error_list: List = list()
        self._default_folder: str = "errors"

    def create_error_manager(self, error_name: str = "") -> bool:
        """
        A method to create the error manager by creating error directory, setting the error name and the filepath

        Args:
            error_name (str, optional): error name will also be used for error file name. Defaults to "".

        Returns:
            bool: True if creating error manager is successful
        """
        # Create Error Directory
        try:
            if not Path.exists(Path(self._default_folder)):
                Path.mkdir(Path(self._default_folder))

            # Initialize the class variables with error object
            if error_name is None:
                file_name_with_log_name = self._name + ".json"
            else:
                error_name_stripped = str(error_name).strip()
                if error_name_stripped == "":
                    file_name_with_log_name = self._name + ".json"
                else:
                    self._name = error_name_stripped
                    file_name_with_log_name = self._name + ".json"

            self._filepath = (
                (Path(self._default_folder) / Path(file_name_with_log_name))
                .absolute()
                .as_posix()
            )

            return True
        except PermissionError:
            return False
        except FileNotFoundError:
            return False

    def add_error_to_list(
        self,
        category: str,
        code: str,
        description: str,
        severity: str,
        origin: str,
        component: str,
    ) -> None:
        """
        A method to create an Error object with the given inputs and
        create an error object and append to the error list.

        Args:
            category (str): error category
            code (str): error code
            description (str): error description
            severity (str): error severity
            origin (str): error origin
            component (str): error component

        Raises:
            RuntimeError: invalid argument because of invalid description, code or component
        """
        # Try to get error info from enum
        try:
            if (
                description == ""
                or description is None
                or code == ""
                or code is None
                or component == ""
                or component is None
            ):
                raise RuntimeError("Invalid description, code or component")

            category = self._get_error_category(category)
            severity = self._get_error_severity(severity)
            origin = self._get_error_origin(origin)

        except RuntimeError as error:
            print(f"Failed creating error due to invalid arguments: {str(error)}")
        else:
            # Create error object
            error_msg = scan_for_single_quotes(description)
            error = Error(category, code, error_msg, severity, origin, component)

            # append this object to the list in the manager class
            self._error_list.append(error)

    def write_error_to_file(self) -> bool:
        """
        A method to write error into the error file

        Returns:
            bool: True if error is written to the file successfully
        """
        try:
            file = open(self._filepath, "w")
            file.write(self.get_errors_as_json_string())
            file.close()
            return True
        except PermissionError:
            return False
        except FileNotFoundError:
            return False

    def get_error_filepath(self) -> str:
        """
        A method to be called by other modules to get the current error path

        Returns:
            str: error filepath
        """
        return self._filepath

    def get_errors_as_json_string(self) -> str:
        """
        A method to return a json string of errors

        Returns:
            str: json string of errors
        """
        json_list = list()
        for error in self._error_list:
            json_list.append(error.get_dict())
        return json.dumps(json_list)

    def get_error_list(self) -> List:
        """
        A method to return the list of errors

        Returns:
            List: error list
        """
        return self._error_list

    def _get_error_category(self, category: str) -> ErrorCategory:
        """
        A helper method to convert the input error category str to enum

        Args:
            category (str): error category

        Raises:
            RuntimeError: invalid category where category is not found in enum

        Returns:
            ErrorCategory: enum value for the given category
        """
        if category == "DAT":
            return ErrorCategory.UNSUPPORTED_DATA
        elif category == "MOD":
            return ErrorCategory.UNSUPPORTED_MODEL
        elif category == "ARG":
            return ErrorCategory.INVALID_ARGUMENT
        elif category == "TST":
            return ErrorCategory.TESTING_FAULT
        elif category == "SYS":
            return ErrorCategory.SYSTEM_ERROR
        else:
            raise RuntimeError(f"Unsupported Error Category: {category}")

    def _get_error_severity(self, severity: str) -> ErrorSeverity:
        """
        A helper method to convert the input error severity str to enum

        Args:
            severity (str): error severity

        Raises:
            RuntimeError: invalid severity where severity is not found in enum

        Returns:
            ErrorSeverity: enum value for the given severity
        """
        if severity == "Information":
            return ErrorSeverity.INFORMATION
        elif severity == "Critical":
            return ErrorSeverity.CRITICAL
        elif severity == "System":
            return ErrorSeverity.SYSTEM_WIDE
        elif severity == "Warning":
            return ErrorSeverity.WARNING
        else:
            raise RuntimeError(f"Unsupported Error Severity: {severity}")

    def _get_error_origin(self, origin: str) -> ErrorOrigin:
        """
        A helper method to convert the input error origin str to enum

        Args:
            origin (str): error origin

        Raises:
            RuntimeError: invalid origin where origin is not found in enum

        Returns:
            ErrorOrigin: enum value for the given origin
        """
        if origin == "User":
            return ErrorOrigin.USER_ERROR
        elif origin == "System":
            return ErrorOrigin.SYSTEM_ERROR
        else:
            raise RuntimeError(f"Unsupported Error Origin: {origin}")
