import queue
from datetime import datetime
from multiprocessing import Lock
from typing import Callable, Dict, Tuple, Union

import pathos
from test_engine_core.interfaces.ialgorithm import IAlgorithm
from test_engine_core.interfaces.idata import IData
from test_engine_core.interfaces.imodel import IModel
from test_engine_core.interfaces.iserializer import ISerializer
from test_engine_core.plugins.enums.plugin_type import PluginType
from test_engine_core.utils.json_utils import remove_numpy_formats, validate_json

from test_engine_app.app_logger import AppLogger
from test_engine_app.enums.task_status import TaskStatus
from test_engine_app.enums.task_type import TaskType
from test_engine_app.processing.iworkerfunction import IWorkerFunction
from test_engine_app.processing.plugin_controller import PluginController
from test_engine_app.processing.task_argument import TaskArgument
from test_engine_app.processing.task_formatter import TaskFormatter
from test_engine_app.processing.task_metadata import TaskMetadata
from test_engine_app.utils.validation_checks import is_empty_string


class Task(IWorkerFunction):
    """
    Task class focuses on storing information and allows data processing and printing results
    regardless of the principle and configuration
    """

    # Class Variables
    lock: Lock = Lock()

    @staticmethod
    def run_algorithm_in_process(
        algorithm_instance: IAlgorithm, results: pathos.helpers.mp.Queue
    ) -> None:
        """
        A static method that runs in a process to generate the results.
        The result will be placed in the queue and returned.

        Args:
            algorithm_instance (IAlgorithm): An instance of IAlgorithm
            results (pathos.helpers.mp.Queue): A queue to store the results and return to the caller
        """
        try:
            # Generate the results using plugin and set task results
            # Update the results in the queue
            algorithm_instance.generate()
            results.put((True, algorithm_instance.get_results()))

        except Exception as exception:
            # Catch all error and Update the exception message in the queue
            results.put((False, str(exception)))

    def __init__(
        self,
        message_id: str,
        message_arguments: str,
        validation_schemas_folder: str,
        task_type: TaskType,
        task_update_cb: Union[Callable, None] = None,
    ):
        # Input parameters
        self._message_id: str = message_id
        self._message_arguments: str = message_arguments
        self._task_type: TaskType = task_type

        # Callback method
        self._task_update_callback: Union[Callable, None] = task_update_cb

        # Task variables
        self._algorithm_process: Union[pathos.helpers.mp.Process, None] = None
        self._task_arguments: TaskArgument = TaskArgument(validation_schemas_folder)
        self._to_cancel: bool = False

        # Task metadata and logging
        self._logger: AppLogger = AppLogger()
        self._metadata: TaskMetadata = TaskMetadata()

        # Task algorith, data, model, ground truth
        self._algorithm_instance: Union[IAlgorithm, None] = None

        self._data_instance: Union[IData, None] = None
        self._data_serializer_instance: Union[ISerializer, None] = None

        self._model_instance: Union[IModel, None] = None
        self._model_serializer_instance: Union[ISerializer, None] = None

        self._ground_truth_instance: Union[IData, None] = None
        self._ground_truth_serializer_instance: Union[ISerializer, None] = None

    def cancel(self) -> None:
        """
        A method to cancel the current operation
        """
        self._logger.raw_logger_instance.info(
            f"Stopping Task: {self._task_arguments.id}"
        )

        # Set flag to cancel
        self._to_cancel = True

        # Check and terminate the process if running
        running_process = self._get_algorithm_process()
        if running_process:
            # Process is running. Terminate it
            running_process.terminate()
        else:
            # Unable to terminate the process
            self._logger.raw_logger_instance.warning("No running task")

    def cleanup(self) -> None:
        """
        A method to perform task clean up
        """
        if self._logger.logger_instance:
            self._logger.logger_instance.stop()

    def get_formatted_results(self) -> Dict:
        """
        A method to return the result for HSET.

        Returns:
            Dict: task result
        """
        # Return the formatted results
        return TaskFormatter.format_response(self._metadata, self._logger.log_filepath)

    def get_id(self) -> str:
        """
        A method to return the task id

        Returns:
            str: task id
        """
        return self._task_arguments.id

    def process(self) -> Tuple[bool, str]:
        """
        A method to run the task to generate the results with the respective algorithm and data inputs
        Print the results to log file
        Write results to the respective output modules

        Returns:
            Tuple[bool, str]: Returns True if processing complete and indicate the error messages if failure
        """
        # Validate the task arguments
        is_success, error_messages = self._task_arguments.parse(self._message_arguments)
        if is_success:
            # Setup task logger
            self._logger.generate_task_logger(self._task_arguments.id)
            self._logger.raw_logger_instance.info(
                f"Task validation successful: {self._task_arguments.id}"
            )

            # Log processing info
            self._logger.raw_logger_instance.info(
                f"Processing Task: "
                f"message_id {self._message_id}, "
                f"message_args {self._message_arguments}, "
                f"task_type: {self._task_type}"
            )

            # Process the incoming task
            if self._task_type is TaskType.PENDING:
                is_success, error_messages = self._process_pending_task()
            else:
                is_success, error_messages = self._process_new_task()

        else:
            # Failed validation
            # Check if id is not None, we can set HSET with error messages
            if not self._task_arguments.id and not is_empty_string(
                self._task_arguments.id
            ):
                # Setup task logger
                self._logger.generate_task_logger(self._task_arguments.id)
                self._logger.raw_logger_instance.info(
                    f"Task validation failed: {self._task_arguments.id}"
                )
                # Add error messages
                self._logger.error_logger_instance.add_error_to_list(
                    "SYS",
                    "WSYSx00002",
                    f"Task Terminated: {error_messages}",
                    "Warning",
                    "System",
                    "task.py",
                )
                # Set task failure
                self._set_task_failure()
            else:
                # Cannot get id value from the message.
                pass

        return is_success, error_messages

    def _get_algorithm_process(self) -> Union[pathos.helpers.mp.Process, None]:
        """
        A helper method to return the running algorithm process

        Returns:
            algorithm_process (Union[pathos.helpers.mp.Process, None]): An algorithm process or None
        """
        with Task.lock:
            # Returns the current algorithm process
            return self._algorithm_process

    def _load_task_instances(self) -> Tuple[bool, str]:
        """
        A helper method to load data, model, ground truth instances

        Returns:
            Tuple[bool, str]: Returns True if load task instance complete and indicate the error messages if failure
        """
        # Identify and load data information
        (
            self._data_instance,
            self._data_serializer_instance,
            _,
        ) = PluginController.get_plugin_instance(
            PluginType.DATA, **{"filename": self._task_arguments.data}
        )
        # log the instance and deserializer
        if self._data_serializer_instance:
            self._logger.raw_logger_instance.info(
                f"Data Instance: {self._data_instance}, "
                f"Data Deserializer: {self._data_serializer_instance.get_serializer_plugin_type()}"
            )
        else:
            self._logger.raw_logger_instance.info(
                f"Data Instance: {self._data_instance}, Data Deserializer: None"
            )
        # perform data setup
        if self._data_instance:
            # Perform data setup
            is_setup_success, error_messages = self._data_instance.setup()
            if is_setup_success:
                pass  # continue
            else:
                return False, f"Unable to setup data instance: {error_messages}"
        else:
            return False, "Unable to get data instance"

        # Identify and load model information
        (
            self._model_instance,
            self._model_serializer_instance,
            _,
        ) = PluginController.get_plugin_instance(
            PluginType.MODEL,
            **{
                "mode": self._task_arguments.mode,
                "filename": self._task_arguments.model,
                "api_schema": self._task_arguments.api_schema,
                "api_config": self._task_arguments.api_config,
            },
        )
        # log the instance and deserializer
        if self._model_serializer_instance:
            self._logger.raw_logger_instance.info(
                f"Model Instance: {self._model_instance}, "
                f"Model Deserializer: {self._model_serializer_instance.get_serializer_plugin_type()}"
            )
        else:
            self._logger.raw_logger_instance.info(
                f"Model Instance: {self._model_instance}, Model Deserializer: None"
            )
        # perform model setup
        if self._model_instance:
            is_setup_success, error_messages = self._model_instance.setup()
            if is_setup_success:
                pass  # continue
            else:
                return False, f"Unable to setup model instance: {error_messages}"
        else:
            return False, "Unable to get model instance"

        # Check if ground_truth is optional
        if (
            self._task_arguments.algorithm_plugin_information.get_algorithm_require_ground_truth()
        ):
            # Require Ground Truth
            (
                self._ground_truth_instance,
                self._ground_truth_serializer_instance,
                _,
            ) = PluginController.get_plugin_instance(
                PluginType.DATA,
                **{"filename": self._task_arguments.ground_truth_dataset},
            )
            # log the instance and deserializer
            if self._ground_truth_serializer_instance:
                self._logger.raw_logger_instance.info(
                    f"GroundTruth Instance: {self._ground_truth_instance}, "
                    f"GroundTruth Deserializer: {self._ground_truth_serializer_instance.get_serializer_plugin_type()}"
                )
            else:
                self._logger.raw_logger_instance.info(
                    f"GroundTruth Instance: {self._ground_truth_instance}, GroundTruth Deserializer: None"
                )
            # perform ground truth setup
            if self._ground_truth_instance:
                is_setup_success, error_messages = self._ground_truth_instance.setup()
                if is_setup_success:
                    pass  # continue
                else:
                    return (
                        False,
                        f"Unable to setup ground truth instance: {error_messages}",
                    )
            else:
                return False, "Unable to get ground truth instance"

            # Leave only the ground truth feature in self._ground_truth_instance and
            # Remove ground truth feature from the data instance
            is_ground_truth_instance_success = (
                self._ground_truth_instance.keep_ground_truth(
                    self._task_arguments.ground_truth
                )
            )
            self._data_instance.remove_ground_truth(self._task_arguments.ground_truth)

            if not is_ground_truth_instance_success:
                return False, "Unable to get ground truth data"
        else:
            # Do not require Ground Truth
            self._ground_truth_instance = None

        # Get the algorithm instance and check if valid instance
        self._algorithm_instance, _, _ = PluginController.get_plugin_instance(
            PluginType.ALGORITHM,
            **{
                "algorithm_id": self._task_arguments.algorithm_id,
                "algorithm_arguments": self._task_arguments.algorithm_arguments,
                "data_instance": self._data_instance,
                "ground_truth_instance": self._ground_truth_instance,
                "ground_truth": self._task_arguments.ground_truth,
                "model_instance": self._model_instance,
                "logger": self._logger.raw_logger_instance,
                "progress_callback": self._update_task_progress,
            },
        )
        if self._algorithm_instance:
            self._logger.raw_logger_instance.info(
                f"Algorithm Instance: {self._algorithm_instance}"
            )
            return True, ""
        else:
            # Algorithm Instance not available
            return False, "Unable to get algorithm instance"

    def _process_new_task(self) -> Tuple[bool, str]:
        """
        A helper method to process on new tasks
        It will run the task and set the respective task response

        Returns:
            Tuple[bool, str]: Returns is_success and indicate the error messages if failure
        """
        is_success: bool = False
        error_messages: str = ""

        try:
            # Set current task as Running and send update
            self._update_task_status(TaskStatus.RUNNING)

            # Load instances
            is_load_success, load_error_messages = self._load_task_instances()
            if not (is_load_success and self._algorithm_instance):
                # Load task instances failed
                raise RuntimeError(load_error_messages)

            # Run the algorithm instance in a Process and will return results when completed.
            # If there is a process termination required, will terminate the process.
            # Create a new queue for the process to place the results
            results_queue = pathos.helpers.mp.Queue()

            # Create the Process
            new_process = pathos.helpers.mp.Process(
                target=Task.run_algorithm_in_process,
                args=(self._algorithm_instance, results_queue),
            )

            # Set the process before starting
            self._set_algorithm_process(new_process)
            new_process.start()
            new_process.join()

            # Retrieve the result from the queue
            try:
                results = results_queue.get(timeout=1)
            except queue.Empty:
                if self._to_cancel:
                    raise RuntimeError("User cancelled")
                else:
                    raise RuntimeError("Algorithm generate no results.")

            # Get the output from the algorithm process
            is_processing_success, process_output = results
            if not is_processing_success:
                # Exception while processing algorithm
                raise RuntimeError(process_output)

            # Get the task results and convert to json friendly and validate against the output schema
            task_results = remove_numpy_formats(process_output)
            is_verify_success, verify_error_messages = self._verify_task_results(
                task_results
            )
            if is_verify_success:
                self._set_task_results(task_results)

                # Update success and error messages
                is_success = True
                error_messages = ""
            else:
                # Validation failed
                raise RuntimeError(verify_error_messages)

        except Exception as exception:
            is_success = False
            error_messages = str(exception)

        finally:
            if is_success:
                # Set current task as success
                self._set_task_success()

            else:
                if is_empty_string(error_messages):
                    error_messages = "Forcefully terminated"

                # Set the error and logs messages
                self._logger.raw_logger_instance.warning(
                    f"Task Terminated: {error_messages}"
                )
                self._logger.error_logger_instance.add_error_to_list(
                    "SYS",
                    "WSYSx00002",
                    f"Task Terminated: {error_messages}",
                    "Warning",
                    "System",
                    "task.py",
                )

                # Set current task as failure / cancelled
                if self._to_cancel:
                    self._set_task_cancelled()
                else:
                    self._set_task_failure()

            # Perform clean up for model instance
            if self._model_instance:
                self._model_instance.cleanup()

        return is_success, error_messages

    def _process_pending_task(self) -> Tuple[bool, str]:
        """
        A helper method to process on pending tasks
        It will write error logs and set the respective task response to set in hset

        Returns:
            Tuple[bool, str]: Returns True and no error messages
        """
        # Set the error and logs messages
        self._logger.raw_logger_instance.info(
            f"Task Terminated: {self._task_arguments.id}"
        )
        self._logger.error_logger_instance.add_error_to_list(
            "SYS",
            "WSYSx00002",
            f"Task Terminated: {self._task_arguments.id}",
            "Warning",
            "System",
            "task.py",
        )

        # Set current task as failure
        self._set_task_failure()

        return True, ""

    def _set_algorithm_process(
        self, algorithm_process: Union[pathos.helpers.mp.Process, None]
    ) -> None:
        """
        A helper method to update the new running algorithm process

        Args:
            algorithm_process (Union[pathos.helpers.mp.Process, None]): An algorithm process or None
        """
        with Task.lock:
            # Set the algorithm process
            self._algorithm_process = algorithm_process

    def _set_task_cancelled(self) -> None:
        """
        A helper method to set the task has cancelled.
        It will write errors found to file, set task end/elapsed, set task percentage and results,
        processState as cancelled.
        """
        # Write error to file
        self._logger.error_logger_instance.write_error_to_file()
        self._metadata.error_messages = (
            self._logger.error_logger_instance.get_errors_as_json_string()
        )

        # Set task percentage and results
        self._metadata.percentage = 100
        self._metadata.results = ""

        # Set the process state to Cancelled and update elapsed time
        self._update_task_status(TaskStatus.CANCELLED)

    def _set_task_failure(self) -> None:
        """
        A helper method to set the task has failed.
        It will write errors found to file, set task end/elapsed, set task percentage and results,
        processState as error.
        """
        # Write error to file
        self._logger.error_logger_instance.write_error_to_file()
        self._metadata.error_messages = (
            self._logger.error_logger_instance.get_errors_as_json_string()
        )

        # Set task percentage and results
        self._metadata.percentage = 100
        self._metadata.results = ""

        # Set the process state to Error and update elapsed time
        self._update_task_status(TaskStatus.ERROR)

    def _set_task_results(self, results: Dict) -> None:
        """
        A helper method to update the new task results

        Args:
            results (Dict): The results to be updated
        """
        # Set the task results
        self._metadata.results = results

    def _set_task_success(self) -> None:
        """
        A helper method to set the task has succeeded.
        It will set task end/elapsed, set task percentage and processState as success.
        """
        # Clear the error messages
        self._metadata.error_messages = ""

        # Set task percentage
        self._metadata.percentage = 100

        # Set the process state to Completed and update elapsed time
        self._update_task_status(TaskStatus.SUCCESS)

    def _send_task_update(self) -> None:
        """
        A helper method to trigger task update for current task
        """
        if self._task_update_callback:
            self._task_update_callback(
                self._task_arguments.id, self.get_formatted_results()
            )

    def _update_elapsed_time(self) -> None:
        """
        A helper method to update the current elapsed time
        """
        # Set task end time and calculate elapsed time
        self._metadata.end_time = datetime.now()
        self._metadata.elapsed_time = int(
            (self._metadata.end_time - self._metadata.start_time).total_seconds()
        )

    def _update_task_progress(self, completion_progress: int) -> None:
        """
        A helper method to update the new task progress and send task update

        Args:
            completion_progress (int): Current progress completion
        """
        # Set the task completion progress
        self._metadata.percentage = completion_progress
        self._logger.raw_logger_instance.info(
            f"Task Completion Progress: {self._message_id} -> {self._metadata.percentage}"
        )

        # Set task end time and calculate elapsed time
        self._update_elapsed_time()

        # Trigger the task callback to send the update
        self._send_task_update()

    def _update_task_status(self, task_status: TaskStatus) -> None:
        """
        A helper method to update the new task status and send task update

        Args:
            task_status (TaskStatus): new task status
        """
        # Set the task status
        self._metadata.status = task_status
        self._logger.raw_logger_instance.info(
            f"Task Status Change: {self._message_id} -> {self._metadata.status}"
        )

        # Set task end time and calculate elapsed time
        self._update_elapsed_time()

        # Trigger the task callback to send the update
        self._send_task_update()

    def _verify_task_results(self, task_result: Dict) -> Tuple[bool, str]:
        """
        A helper method to validate the task results according to the output schema

        Args:
            task_result (Dict): A dictionary of results generated by the algorithm

        Returns:
            Tuple[bool, str]: True if validated, False if validation failed.
        """
        is_success = True
        error_message = ""

        # Check that results type is dict
        if type(task_result) is not dict:
            # Raise error - wrong type
            is_success = False
            error_message = f"Invalid type for results: {type(task_result).__name__}"

        else:
            # Validate the json result with the relevant schema.
            # Check that it meets the required format before sending out to the UI for display
            if not validate_json(
                task_result,
                self._task_arguments.algorithm_plugin_information.get_algorithm_output_schema(),
            ):
                is_success = False
                error_message = "Failed schema validation"

        return is_success, error_message
