from logging import Logger
from typing import Any, Dict, Tuple, Union

from test_engine_core.interfaces.idata import IData
from test_engine_core.interfaces.iserializer import ISerializer


class DataManager:
    """
    The DataManager comprises methods that focuses on reading data files
    As input files are usually serialized before written to a file, this class will perform
    de-serialisation with supported packages, and identify if the data is one of the supported formats
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
        DataManager._logger = logger

    @staticmethod
    def read_data_file(
        data_file: str, data_plugins: Dict, serializer_plugins: Dict
    ) -> Tuple[bool, Union[IData, None], Union[ISerializer, None], str]:
        """
        A method to read the data file path and return the data instance and serializer instance
        It is usually serialize by some program such as (pickle, joblib)

        Args:
            data_file (str): The data file path
            data_plugins (Dict): The dictionary of detected data plugins
            serializer_plugins (Dict): The dictionary of detected serializer plugins

        Returns:
            Tuple[bool, Union[IData, None], Union[ISerializer, None], str]:
            True if success, False if failed to deserialize / identify data file
        """
        # Attempt to deserialize the data with the supported serializer.
        # If data is not able to be deserialized by any of the supported tool, it will return False
        if DataManager._logger is not None:
            DataManager._logger.debug(f"Attempting to deserialize data: {data_file}")

        is_success, data, serializer_instance = DataManager._try_to_deserialize_data(
            data_file, serializer_plugins
        )
        if is_success:
            if DataManager._logger is not None:
                DataManager._logger.debug(
                    f"Attempting to identify data format: {type(data)}"
                )

            # Attempt to identify the data format with the supported list.
            # If data is not in the supported list, it will return False
            is_success, data_instance = DataManager._try_to_identify_data_format(
                data, data_plugins
            )
            if is_success:
                error_message = ""
                # Perform logging
                if DataManager._logger is not None:
                    DataManager._logger.debug(
                        f"Supported data format: {type(data)} -> {data_instance.get_plugin_type()}"
                    )
            else:
                # Failed to get data format
                data_instance = None
                error_message = f"Unsupported data format: {type(data)}"
                # Perform logging
                if DataManager._logger is not None:
                    DataManager._logger.error(error_message)
        else:
            # Failed to deserialize data file
            data_instance = None
            serializer_instance = None
            error_message = f"Failed to deserialize dataset: {data_file}"
            # Perform logging
            if DataManager._logger is not None:
                DataManager._logger.error(error_message)

        return is_success, data_instance, serializer_instance, error_message

    @staticmethod
    def _try_to_deserialize_data(
        data_file: str, serializer_plugins: Dict
    ) -> Tuple[bool, Any, Any]:
        """
        A helper method to deserialize the data file path and return the de-serialized data and serializer instance

        Args:
            data_file (str): The data file path
            serializer_plugins (Dict): The dictionary of detected serializer plugins

        Returns:
            Tuple[bool, Any, Any]: True if success, False if failed to deserialize data file
        """
        is_success = False
        data = None
        serializer = None

        # Scan through all the supported serializer
        # Check that this data is one of the supported data formats and can be deserialized
        for (
            serializer_plugin_name,
            serializer_plugin,
        ) in serializer_plugins.items():
            try:
                serializer = serializer_plugin.Plugin
                data = serializer.deserialize_data(data_file)
                is_success = True
                break
            except Exception:
                continue

        return is_success, data, serializer

    @staticmethod
    def _try_to_identify_data_format(
        data: Any, data_plugins: Dict
    ) -> Tuple[bool, IData]:
        """
        A helper method to read the data and return the respective data format instance

        Args:
            data (Any): The de-serialized data
            data_plugins (Dict): The dictionary of detected data plugins

        Returns:
            Tuple[bool, IData]: True if data format is supported
        """
        is_success = False
        data_instance = None

        # Scan through all the supported data formats
        # Check that this data is one of the supported data formats
        for data_plugin_name, data_plugin in data_plugins.items():
            data_instance = data_plugin.Plugin(data)
            if data_instance.is_supported():
                is_success = True
                break

        return is_success, data_instance
