import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, Union

from test_engine_core.plugins.enums.model_mode_type import ModelModeType
from test_engine_core.utils.json_utils import load_schema_file, validate_json

from test_engine_app.utils.validation_checks import is_empty_string, is_file, is_folder


@dataclass
class ValidateModelArgument:
    """
    ValidateModelArgument class comprises ValidateModel service arguments information
    It also provides methods for validation and parsing service arguments
    """

    # Service ID
    id: Union[str, None]

    # Model Validation Arguments
    model_mode: Union[ModelModeType, None]
    model_path: Union[str, None]
    api_schema: Dict
    api_config: Dict

    def __init__(self, validation_schema_folder: str):
        self.id = None
        self.model_mode = None
        self.model_path = None
        self.api_schema = dict()
        self.api_config = dict()
        self._validation_schema_file = str(
            Path(validation_schema_folder) / "test_engine_validate_model_schema.json"
        )
        self._validation_schema = None

    def parse(self, args: str) -> Tuple[bool, str]:
        """
        A function to read the message arguments, validate the information

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
                self.model_path = args_dict.get("filePath")
                if args_dict.get("mode") == ModelModeType.API.name.lower():
                    self.model_mode = ModelModeType.API
                elif args_dict.get("mode") == ModelModeType.UPLOAD.name.lower():
                    self.model_mode = ModelModeType.UPLOAD
                else:
                    return (
                        False,
                        "Model mode type unsupported. Supported model modes are API and UPLOAD.",
                    )

                # Perform args validation
                error_count, error_message = self.validate()
                if error_count == 0:
                    return True, ""
                else:
                    return False, error_message

            else:
                # Attempt to get id despite failed validation.
                self.id = args_dict.get("serviceId")
                return (
                    False,
                    f"Failed TestEngineService validateModel input schema validation for {self.id}",
                )

        except Exception as error:
            return False, str(error)

    def validate(self) -> Tuple[int, str]:
        """
        A function to validate the task arguments are within bounds

        Returns:
            Tuple[int, str]: Returns error count and error messages
        """
        error_count = 0
        error_message = ""

        # Perform Validation
        if self.model_mode is ModelModeType.API:
            validation_functions = [self._validate_model_mode, self._validate_model_api]
        else:
            validation_functions = [
                self._validate_model_mode,
                self._validate_model_upload,
            ]

        for func in validation_functions:
            tmp_count, tmp_error_msg = func()
            error_count += tmp_count
            error_message += tmp_error_msg

        return error_count, error_message

    def _validate_model_mode(self) -> Tuple[int, str]:
        """
        A helper function to validate model mode

        Returns:
            Tuple[int, str]: Returns error count and error messages
        """
        error_count = 0
        error_message = ""

        if not (isinstance(self.model_mode, ModelModeType)):
            error_count += 1
            error_message += "Invalid model mode;"

        return error_count, error_message

    def _validate_model_upload(self) -> Tuple[int, str]:
        """
        A helper method to validate model-upload

        Returns:
            Tuple[int, str]: Returns error count and error messages
        """
        error_count = 0
        error_message = ""

        # If model is tf, the path should be a folder, else it is a file.
        # As long as the model exists either a file or model, we pass it first. Will check when detected.
        if type(self.model_path) is not str:
            error_count += 1
            error_message += "Model file is not a string;"
        elif is_empty_string(self.model_path):
            error_count += 1
            error_message += "Model file is empty string;"
        else:
            if not (is_file(self.model_path) or is_folder(Path(self.model_path))):
                error_count += 1
                error_message += "Model file not found;"

        return error_count, error_message

    def _validate_model_api(self) -> Tuple[int, str]:
        """
        A helper method to validate model-api

        Returns:
            Tuple[int, str]: Returns error count and error messages
        """
        error_count = 0
        error_message = ""

        if type(self.api_schema) is not dict:
            error_count += 1
            error_message += "Api Schema is not a dict;"

        if type(self.api_config) is not dict:
            error_count += 1
            error_message += "Api Config is not a dict;"

        return error_count, error_message
