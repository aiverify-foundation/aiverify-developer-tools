import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, Union

from test_engine_core.utils.json_utils import load_schema_file, validate_json

from test_engine_app.utils.validation_checks import is_empty_string, is_file


@dataclass
class ValidateDatasetArgument:
    """
    ValidateDatasetArgument class comprises ValidateDataset service arguments information
    It also provides methods for validation and parsing service arguments
    """

    # Service ID
    id: Union[str, None]

    # Dataset Validation Arguments
    data_path: Union[str, None]

    def __init__(self, validation_schema_folder: str):
        self.id = None
        self.data_path = None
        self._validation_schema_file = str(
            Path(validation_schema_folder) / "test_engine_validate_dataset_schema.json"
        )
        self._validation_schema = None

    def parse(self, args: str) -> Tuple[bool, str]:
        """
        A method to read the message arguments, validate the information

        Args:
            args (str): message arguments

        Returns:
            Tuple[bool, str]: True if parsed successfully, else return False and error message
        """
        try:
            # Load the validation schema and JSON str
            self._validation_schema = load_schema_file(self._validation_schema_file)
            args_dict: Dict = json.loads(args)

            # Perform JSON Validation on the schema.
            if validate_json(args_dict, self._validation_schema):
                # Required fields
                self.id = args_dict.get("serviceId")
                self.data_path = args_dict.get("filePath")

                # Perform args validation
                error_count, error_message = self.validate()
                if error_count == 0:
                    return True, error_message
                else:
                    return False, error_message

            else:
                # Attempt to get id despite failed validation.
                self.id = args_dict.get("serviceId")
                return (
                    False,
                    "Failed TestEngineService validateDataset input schema validation",
                )

        except RuntimeError as error:
            return False, str(error)

    def validate(self) -> Tuple[int, str]:
        """
        A method to validate the task arguments are within bounds

        Returns:
            Tuple[int, str]: Returns error count and error messages
        """
        error_count = 0
        error_message = ""

        validation_functions = [self._validate_data]

        for func in validation_functions:
            tmp_count, tmp_error_msg = func()
            error_count += tmp_count
            error_message += tmp_error_msg

        return error_count, error_message

    def _validate_data(self) -> Tuple[int, str]:
        """
        A helper method to validate data file

        Returns:
            Tuple[int, str]: Returns error count and error messages
        """
        error_count = 0
        error_message = ""

        if type(self.data_path) is not str:
            error_count += 1
            error_message += "Data file is not a string;"
        elif is_empty_string(self.data_path):
            error_count += 1
            error_message += "Data file is empty string;"
        else:
            if not is_file(self.data_path):
                error_count += 1
                error_message += "Data file not found;"

        return error_count, error_message
