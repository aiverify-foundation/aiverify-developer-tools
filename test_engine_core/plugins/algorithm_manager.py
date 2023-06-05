from logging import Logger
from pathlib import Path
from typing import Dict, Tuple, Union

from test_engine_core.interfaces.ialgorithm import IAlgorithm


class AlgorithmManager:
    """
    The AlgorithmManager comprises methods that focuses on finding algorithm from the supported algorithm plugins.
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
        AlgorithmManager._logger = logger

    @staticmethod
    def get_algorithm(
        algorithm_plugins: Dict, **kwargs
    ) -> Tuple[bool, Union[IAlgorithm, None], str]:
        """
        A method to retrieve the algorithm with the algoId and return the algorithm instance.

        Args:
            algorithm_plugins (Dict): The dictionary of supported algorithm plugins

        Returns:
            Tuple[bool, Union[IAlgorithm, None], str]:
            True if success, False if failed to find algorithm
        """
        # Get required information
        algorithm_id = kwargs.get("algorithm_id", "")
        algorithm_arguments = kwargs.get("algorithm_arguments", dict())
        data_instance = kwargs.get("data_instance", None)
        ground_truth_instance = kwargs.get("ground_truth_instance", None)
        model_instance = kwargs.get("model_instance", None)

        # Search through the algorithm list and get an instance
        if algorithm_id in algorithm_plugins.keys():
            # Found the algorithm in our detected list
            is_success = True
            error_message = ""

            # Update the base path and create an instance of the plugin
            algorithm_arguments["project_base_path"] = Path(
                algorithm_plugins[algorithm_id].__file__
            ).parent
            algorithm_arguments["logger"] = kwargs.get("logger", None)
            algorithm_arguments["progress_callback"] = kwargs.get(
                "progress_callback", None
            )
            algorithm_arguments["ground_truth"] = kwargs.get("ground_truth", "")
            algorithm = algorithm_plugins[algorithm_id].Plugin(
                data_instance,
                model_instance,
                ground_truth_instance,
                **algorithm_arguments,
            )

            # Perform logging
            if AlgorithmManager._logger is not None:
                AlgorithmManager._logger.debug(
                    f"Supported algorithm: {algorithm_id} -> {algorithm.get_plugin_type()}"
                )

        else:
            algorithm = None
            is_success = False
            error_message = f"Unsupported algorithm: {algorithm_id}"

            # Perform logging
            if AlgorithmManager._logger is not None:
                AlgorithmManager._logger.error(error_message)

        return is_success, algorithm, error_message
