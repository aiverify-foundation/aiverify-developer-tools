from logging import Logger
from typing import Any, Dict, Tuple, Union

from test_engine_core.interfaces.imodel import IModel
from test_engine_core.interfaces.iserializer import ISerializer


class ModelManager:
    """
    The ModelManager comprises methods that focuses on reading model files
    As input files are usually serialized before written to a file, this class will perform
    de-serialisation with supported packages, and identify if the model is one of the supported formats
    """

    # Class Variables
    _logger: Logger = None

    @staticmethod
    def set_logger(logger: Logger) -> None:
        """
        A method to set up the logger instance for logging

        Args:
            logger (Logger): The logger instance

        """
        ModelManager._logger = logger

    @staticmethod
    def read_model_api(
        api_schema: Dict, api_config: Dict, model_plugins: Dict
    ) -> Tuple[bool, Union[IModel, None], Union[ISerializer, None], str]:
        """
        A method to read the model api schema and config and return the model_instance and serializer instance

        Args:
            api_schema (Dict): Input api schema information
            api_config (Dict): Input api config information
            model_plugins (Dict): The dictionary of detected model plugins

        Returns:
            Tuple[bool, Union[IModel, None], Union[ISerializer, None], str]:
            True if successful, False if failed to set up
        """
        serializer_instance = None

        if ModelManager._logger is not None:
            ModelManager._logger.debug(
                f"Attempting to read model api: api_schema: {api_schema}, api_config: {api_config}"
            )

        is_success, model_instance = ModelManager._try_to_identify_model_format(
            None, model_plugins, api_schema, api_config
        )
        if is_success:
            error_message = ""
            # Perform logging
            if ModelManager._logger is not None:
                ModelManager._logger.debug(
                    f"Supported model format: {model_instance.get_plugin_type()}"
                )
        else:
            model_instance = None
            error_message = "Unsupported model format"
            # Perform logging
            if ModelManager._logger is not None:
                ModelManager._logger.error(error_message)

        return is_success, model_instance, serializer_instance, error_message

    @staticmethod
    def read_model_file(
        model_file: str, model_plugins: Dict, serializer_plugins: Dict
    ) -> Tuple[bool, Union[IModel, None], Union[ISerializer, None], str]:
        """
        A method to read the model file path and return the model instance and serializer instance
        It is usually serialize by some program such as (pickle, joblib)

        Args:
            model_file (str): The model file path
            model_plugins (Dict): The dictionary of detected model plugins
            serializer_plugins (Dict): The dictionary of detected serializer plugins

        Returns:
            Tuple[bool, Union[IModel, None], Union[ISerializer, None], str]:
            True if success, False if failed to deserialize / identify model file
        """
        # Attempt to deserialize the model with the supported serializer.
        # If model is not able to be deserialized by any of the supported tool, it will return False
        if ModelManager._logger is not None:
            ModelManager._logger.debug(f"Attempting to deserialize model: {model_file}")

        is_success, model, serializer_instance = ModelManager._try_to_deserialize_model(
            model_file, serializer_plugins
        )
        if is_success:
            if ModelManager._logger is not None:
                ModelManager._logger.debug(
                    f"Attempting to identify model format: {type(model)}"
                )

            # Attempt to identify the model format with the supported list.
            # If model is not in the supported list, it will return False
            is_success, model_instance = ModelManager._try_to_identify_model_format(
                model, model_plugins
            )
            if is_success:
                error_message = ""
                # Perform logging
                if ModelManager._logger is not None:
                    ModelManager._logger.debug(
                        f"Supported model format: {type(model)} -> "
                        f"{model_instance.get_plugin_type()}[{model_instance.get_model_algorithm()}]"
                    )
            else:
                # Failed to get model format
                model_instance = None
                error_message = f"Unsupported model format: {type(model)}"
                # Perform logging
                if ModelManager._logger is not None:
                    ModelManager._logger.error(error_message)
        else:
            # Failed to deserialize model file
            model_instance = None
            serializer_instance = None
            error_message = f"Failed to deserialize model: {model_file}"
            # Perform logging
            if ModelManager._logger is not None:
                ModelManager._logger.error(error_message)

        return is_success, model_instance, serializer_instance, error_message

    @staticmethod
    def _try_to_deserialize_model(
        model_file: str, serializer_plugins: Dict
    ) -> Tuple[bool, Any, Any]:
        """
        A helper method to deserialize the model file path and return the de-serialized model and serializer instance

        Args:
            model_file (str): The model file path
            serializer_plugins (Dict): The dictionary of detected serializer plugins

        Returns:
            Tuple[bool, Any, Any]: True if success, False if failed to deserialize model file
        """
        is_success = False
        model = None
        serializer = None

        # Scan through all the supported serializer
        # Check that this model is one of the supported model formats and can be deserialized
        for (
            serializer_plugin_name,
            serializer_plugin,
        ) in serializer_plugins.items():
            try:
                serializer = serializer_plugin.Plugin
                model = serializer.deserialize_data(model_file)
                is_success = True
                break
            except Exception:
                continue

        return is_success, model, serializer

    @staticmethod
    def _try_to_identify_model_format(
        model: Any,
        model_plugins: Dict,
        api_schema: Dict = None,
        api_config: Dict = None,
    ) -> Tuple[bool, IModel]:
        """
        A helper method to read the model and return the respective model format instance

        Args:
            model (Any): The de-serialized model
            model_plugins (Dict): The dictionary of detected model plugins

        Returns:
            Tuple[bool, IModel]: True if model format is supported
        """
        is_success = False
        model_instance = None

        # Scan through all the supported model formats
        # Check that this model is one of the supported model formats
        for model_plugin_name, model_plugin in model_plugins.items():
            if api_schema is None and api_config is None:
                model_instance = model_plugin.Plugin(model)
            else:
                model_instance = model_plugin.Plugin(model, api_schema, api_config)

            if model_instance.is_supported():
                is_success = True
                break

        return is_success, model_instance
