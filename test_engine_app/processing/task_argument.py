import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, Union

from test_engine_core.plugins.enums.model_mode_type import ModelModeType
from test_engine_core.plugins.enums.model_type import ModelType
from test_engine_core.plugins.enums.plugin_type import PluginType
from test_engine_core.utils.json_utils import load_schema_file, validate_json

from test_engine_app.processing.algorithm_info import AlgorithmInfo
from test_engine_app.processing.plugin_controller import PluginController
from test_engine_app.utils.validation_checks import is_empty_string, is_file, is_folder


@dataclass
class TaskArgument:
    """
    TaskArgument class comprises task arguments information
    It also provides methods for validation and parsing task arguments
    """

    # Task ID
    id: Union[str, None]

    # Dataset Arguments
    data: Union[str, None]

    # Ground Truth Arguments
    ground_truth_dataset: Union[str, None]
    ground_truth: Union[str, None]

    # Model Arguments
    api_schema: Union[Dict, None]
    api_config: Union[Dict, None]
    mode: Union[ModelModeType, None]
    model: Union[str, None]
    model_type: Union[ModelType, None]

    # Algorithm Arguments
    algorithm_id: Union[str, None]
    algorithm_arguments: Union[Dict, None]

    # Others
    algorithm_plugin_information: Union[AlgorithmInfo, None]
    _validation_schema_file: Union[str, None]
    _validation_schema: Union[Dict, None]

    def __init__(self, validation_schema_folder: str):
        # Set default value as None
        self.id = None
        self.data = None
        self.ground_truth_dataset = None
        self.ground_truth = None
        self.api_schema = None
        self.api_config = None
        self.mode = None
        self.model = None
        self.model_type = None
        self.algorithm_id = None
        self.algorithm_arguments = None
        self.algorithm_plugin_information = None
        self._validation_schema_file = str(
            Path(validation_schema_folder) / "test_engine_task_schema.json"
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
                # Validated Ok
                # Required fields
                self.id = args_dict.get("id")
                self.data = args_dict.get("testDataset")
                self.algorithm_id = args_dict.get("algorithmId")
                self.algorithm_arguments = args_dict.get("algorithmArgs")
                if args_dict.get("mode") == ModelModeType.API.name.lower():
                    self.mode = ModelModeType.API
                else:
                    self.mode = ModelModeType.UPLOAD

                # API/UPLOAD (Optional)
                self.api_schema = args_dict.get("apiSchema")
                self.api_config = args_dict.get("apiConfig")
                self.model = args_dict.get("modelFile")

                # ModelType (Optional)
                if args_dict.get("modelType") == ModelType.CLASSIFICATION.name.lower():
                    self.model_type = ModelType.CLASSIFICATION
                elif args_dict.get("modelType") == ModelType.REGRESSION.name.lower():
                    self.model_type = ModelType.REGRESSION
                else:
                    self.model_type = None

                # GroundTruth (Optional)
                self.ground_truth_dataset = args_dict.get("groundTruthDataset")
                self.ground_truth = args_dict.get("groundTruth")

                # Retrieve the algorithm plugin information
                self.algorithm_plugin_information = (
                    PluginController.get_plugin_information(
                        PluginType.ALGORITHM, **{"algorithm_id": self.algorithm_id}
                    )
                )

                # Perform args validation
                error_count, error_message = self.validate()
                if error_count == 0:
                    return True, error_message
                else:
                    return False, error_message

            else:
                # Attempt to get id despite failed validation.
                self.id = args_dict.get("id")
                return False, "Failed TestEngineTask input schema validation"

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

        # Perform Validation
        if self.mode is ModelModeType.API:
            validation_methods = [
                self._validate_data,
                self._validate_model_api,
                self._validate_algorithm,
            ]
        else:
            validation_methods = [
                self._validate_data,
                self._validate_model_upload,
                self._validate_algorithm,
            ]

        for method in validation_methods:
            tmp_count, tmp_error_msg = method()
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

        if type(self.data) is not str:
            error_count += 1
            error_message += "Data file is not a string;"
        elif is_empty_string(self.data):
            error_count += 1
            error_message += "Data file is empty string;"
        else:
            if not is_file(self.data):
                error_count += 1
                error_message += "Data file not found;"

        return error_count, error_message

    def _validate_ground_truth(self) -> Tuple[int, str]:
        """
        A helper method to validate ground truth

        Returns:
            Tuple[int, str]: Returns error count and error messages
        """
        error_count = 0
        error_message = ""

        # Ground Truth Dataset is defined.
        if type(self.ground_truth_dataset) is not str:
            error_count += 1
            error_message += "Ground Truth dataset file is not a string;"
        elif is_empty_string(self.ground_truth_dataset):
            error_count += 1
            error_message += "Ground Truth dataset file is empty string;"
        else:
            if not is_file(self.ground_truth_dataset):
                error_count += 1
                error_message += "Ground Truth dataset file not found;"

        # Ground Truth is defined
        if type(self.ground_truth) is not str:
            error_count += 1
            error_message += "Ground Truth is not a string;"
        elif is_empty_string(self.ground_truth):
            error_count += 1
            error_message += "Ground Truth is empty string;"

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
        if type(self.model) is not str:
            error_count += 1
            error_message += "Model file is not a string;"
        elif is_empty_string(self.model):
            error_count += 1
            error_message += "Model file is empty string;"
        else:
            if not (is_file(self.model) or is_folder(Path(self.model))):
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

    def _validate_algorithm(self) -> Tuple[int, str]:
        """
        A helper method to validate algorithm id and input arguments

        Returns:
            Tuple[int, str]: Returns error count and error messages
        """
        error_count = 0
        error_message = ""

        if self.algorithm_plugin_information:
            # Get the algorithm input schema and validate the algorithm arguments
            if validate_json(
                self.algorithm_arguments,
                self.algorithm_plugin_information.get_algorithm_input_schema(),
            ):
                # Validate Ground Truth
                if (
                    self.algorithm_plugin_information.get_algorithm_require_ground_truth()
                ):
                    if not self.ground_truth or not self.ground_truth_dataset:
                        error_count += 1
                        error_message += "Ground truth validation failed;"
                    else:
                        # Both ground truth exists.
                        error_count, error_message = self._validate_ground_truth()
                else:
                    pass  # Ground truth not required. values don't matter.
            else:
                error_count += 1
                error_message += "Algorithm arguments validation failed;"
        else:
            error_count += 1
            error_message += "Algorithm ID is not found;"

        return error_count, error_message
