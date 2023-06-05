from typing import Callable, Dict, List, Tuple, Union

from test_engine_core.interfaces.idata import IData
from test_engine_core.plugins.enums.data_plugin_type import DataPluginType
from test_engine_core.plugins.enums.plugin_type import PluginType
from test_engine_core.plugins.enums.serializer_plugin_type import SerializerPluginType

from test_engine_app.app_logger import AppLogger
from test_engine_app.enums.service_result import ServiceResult
from test_engine_app.enums.service_status import ServiceStatus
from test_engine_app.enums.task_type import TaskType
from test_engine_app.processing.iworkerfunction import IWorkerFunction
from test_engine_app.processing.plugin_controller import PluginController
from test_engine_app.processing.service_formatter import ServiceFormatter
from test_engine_app.processing.service_metadata import ServiceMetadata
from test_engine_app.processing.validate_dataset_argument import ValidateDatasetArgument


class ValidateDataset(IWorkerFunction):
    """
    ValidateDataset class focuses on storing information and allows data processing and
    printing results of dataset validation
    """

    def __init__(
        self,
        message_id: str,
        message_arguments: str,
        validation_schemas_folder: str,
        task_type: TaskType,
        service_update_cb: Union[Callable, None] = None,
    ):
        # Input parameters
        self._message_id: str = message_id
        self._message_arguments: str = message_arguments
        self._task_type: TaskType = task_type

        self._service_update_callback: Union[Callable, None] = service_update_cb

        # Service variables
        self._service_arguments: ValidateDatasetArgument = ValidateDatasetArgument(
            validation_schemas_folder
        )

        # Service metadata and logging
        self._logger: AppLogger = AppLogger()
        self._metadata: ServiceMetadata = ServiceMetadata()

        self._temp_results: str = ""
        self._data_labels: str = ""
        self._json_array: List = list()

        # Service data
        self._data_instance: Union[IData, None] = None

    def cleanup(self) -> None:
        """
        Performs service clean up
        """
        if self._logger.logger_instance:
            self._logger.logger_instance.stop()

    def get_formatted_results(self) -> Dict:
        """
        A method to return the result for HSET.

        Returns:
            Dict: service result
        """
        # Return the formatted results
        return ServiceFormatter.format_dataset_validation_response(
            self._metadata, self._logger.log_filepath
        )

    def get_id(self) -> str:
        """
        A method to return the service id

        Returns:
            str: service id
        """
        return self._service_arguments.id

    def process(self) -> Tuple[bool, str]:
        """
        A method to run the service to generate the validation results
        Print the results to log file
        Write results to the respective output modules

        Returns:
            Tuple[bool, str]: Returns True if processing complete and indicate the error messages if failure
        """
        # Validate the service arguments
        is_success, error_messages = self._service_arguments.parse(
            self._message_arguments
        )
        if is_success:
            # Setup logger
            self._logger.generate_task_logger(self._service_arguments.id)
            self._logger.raw_logger_instance.info(
                f"Service message successful: {self._service_arguments.id}"
            )

            # Log processing info
            self._logger.raw_logger_instance.info(
                f"Processing dataset validation service: "
                f"message_id {self._message_id}, "
                f"message_args {self._message_arguments}, "
                f"task_type: {self._task_type}"
            )

            # Process the incoming service
            try:
                if self._task_type is TaskType.PENDING:
                    is_success, error_messages = self._process_pending_service()
                else:
                    is_success, error_messages = self._process_new_service()

            except Exception as exception:
                is_success = False
                error_messages = str(exception)

                # Set the error and logs messages
                self._logger.raw_logger_instance.warning(
                    f"Service Terminated: {error_messages}"
                )
                self._logger.error_logger_instance.add_error_to_list(
                    "SYS",
                    "WSYSx00002",
                    f"Service Terminated: {self._service_arguments.id}",
                    "Warning",
                    "System",
                    "validate_dataset.py",
                )

                # Set current service as failure
                self._set_service_failure()
        else:
            # Setup logger
            self._logger.generate_task_logger(self._service_arguments.id)
            self._logger.raw_logger_instance.warning(
                f"Service Terminated: {error_messages}"
            )
            self._logger.error_logger_instance.add_error_to_list(
                "SYS",
                "WSYSx00002",
                f"Service Terminated: {error_messages}",
                "Warning",
                "System",
                "validate_dataset.py",
            )

        return is_success, error_messages

    def _process_new_service(self) -> Tuple[bool, str]:
        """
        A helper method to process on new services
        It will run the service and set the respective service response

        Returns:
            Tuple[bool, str]: Returns is_success and indicate the error messages if failure
        """
        is_success: bool = False
        error_messages: str = ""

        try:
            # Set current service as Running and send update
            self._set_and_send_service_status(ServiceStatus.RUNNING)

            # Identify, Load the model, serialiser and error messages
            (
                self._data_instance,
                self._serializer_instance,
                self._error_message,
            ) = PluginController.get_plugin_instance(
                PluginType.DATA, **{"filename": self._service_arguments.data_path}
            )

            if not self._data_instance:
                error_messages = self._error_message
                self._logger.raw_logger_instance.warning(
                    f"Service Terminated: {error_messages}"
                )
                self._logger.error_logger_instance.add_error_to_list(
                    "DAT",
                    "WDATx00002",
                    f"{error_messages}",
                    "Warning",
                    "System",
                    "validate_dataset.py",
                )
                is_success = True
                self._set_file_invalid()

            else:
                # Validate dataset
                is_data_valid, validation_error_message = self._data_instance.validate()

                if is_data_valid:
                    # Get dataset features, serializer type and data format
                    if not self._data_instance.read_labels():
                        error_messages = "Dataset is empty"
                        self._logger.raw_logger_instance.warning(
                            f"Service Terminated: {error_messages}"
                        )
                        self._logger.error_logger_instance.add_error_to_list(
                            "DAT",
                            "WDATx00002",
                            f"{error_messages}",
                            "Warning",
                            "System",
                            "validate_dataset.py",
                        )
                        is_success = True
                        self._set_file_invalid()

                    else:
                        # Get dataset features and write with serializer type and data format to results
                        for key, value in self._data_instance.read_labels().items():
                            self._json_array.append({"name": key, "datatype": value})
                        self._set_service_results(
                            self._json_array,
                            self._serializer_instance.get_serializer_plugin_type(),
                            self._data_instance.get_data_plugin_type(),
                        )
                        is_success = True
                        self._set_file_valid()

                else:
                    error_messages = validation_error_message
                    self._logger.raw_logger_instance.warning(
                        f"Service Terminated: {error_messages}"
                    )
                    self._logger.error_logger_instance.add_error_to_list(
                        "DAT",
                        "WDATx00002",
                        f"{error_messages}",
                        "Warning",
                        "System",
                        "validate_dataset.py",
                    )
                    is_success = True
                    self._set_file_invalid()

        except Exception as exception:
            # Failed validation, failure info in error message
            error_messages = str(exception)

            # Set the error and logs messages
            self._logger.raw_logger_instance.warning(
                f"Service Terminated: {error_messages}"
            )
            self._logger.error_logger_instance.add_error_to_list(
                "SYS",
                "WSYSx00002",
                f"Service Terminated: {error_messages}",
                "Warning",
                "System",
                "validate_dataset.py",
            )

            # Set validation complete and set file as invalid
            is_success = False
            self._set_service_failure()

        return is_success, error_messages

    def _process_pending_service(self) -> Tuple[bool, str]:
        """
        A helper method to process on pending services
        It will write error logs and set the respective service response to set in hset

        Returns:
            Tuple[bool, str]: Returns True and no error messages
        """
        # Set the error and logs messages
        self._logger.raw_logger_instance.info(
            f"Service Terminated: {self._service_arguments.id}"
        )
        self._logger.error_logger_instance.add_error_to_list(
            "SYS",
            "WSYSx00002",
            f"Service Terminated: {self._service_arguments.id}",
            "Warning",
            "System",
            "validate_dataset.py",
        )

        # Set current service as failure
        self._set_service_failure()

        return True, ""

    def _set_service_results(
        self,
        schema: List,
        serializer_type: SerializerPluginType,
        data_format: DataPluginType,
    ) -> None:
        """
        A helper method to update the new service results

        Args:
            schema (List): Column schema extracted from dataset
            serializer_type (SerializerPluginType): Name of the serializer type
            data_format (DataPluginType): Name of the data format
        """

        self._logger.raw_logger_instance.info(
            f"Schema extracted: {schema} , serializer type: {serializer_type.name} , "
            f"and data type: {data_format.name} writing to metadata..."
        )

        self._metadata.schema = schema
        self._metadata.serializer_type = serializer_type
        self._metadata.data_format = data_format

    def _set_service_failure(self) -> None:
        """
        A helper method to set the service as ERROR.
        It will write errors found to file and set validation result as null.
        """
        # Write error to file
        self._logger.error_logger_instance.write_error_to_file()
        self._metadata.error_messages = (
            self._logger.error_logger_instance.get_errors_as_json_string()
        )

        self._metadata.result = ServiceResult.NONE

        # Set the process state to Error
        self._set_and_send_service_status(ServiceStatus.ERROR)

    def _set_file_invalid(self) -> None:
        """
        A helper method to set the service as DONE and validation results as invalid.
        It will write errors found to file and set validation result as invalid.
        """
        # Write error to file
        self._logger.error_logger_instance.write_error_to_file()
        self._metadata.error_messages = (
            self._logger.error_logger_instance.get_errors_as_json_string()
        )

        self._metadata.result = ServiceResult.INVALID

        # Set the process state to Done
        self._set_and_send_service_status(ServiceStatus.DONE)

    def _set_file_valid(self) -> None:
        """
        A helper method to set the service as DONE and validation results as valid.
        It will write errors found to file and set validation result as valid.
        """
        self._metadata.error_messages = ""
        self._metadata.result = ServiceResult.VALID

        # Set the process state to Done
        self._set_and_send_service_status(ServiceStatus.DONE)

    def _set_and_send_service_status(self, service_status: ServiceStatus) -> None:
        """
        A helper method to set the new service status and send service update

        Args:
            service_status (ServiceStatus): new service status
        """
        # Set the service status
        self._metadata.status = service_status
        self._logger.raw_logger_instance.info(
            f"Service Status Change: {self._message_id} -> {self._metadata.status}"
        )

        # Trigger the service callback to send the update
        self._send_service_update()

    def _send_service_update(self) -> None:
        """
        A helper method to trigger service update for current service
        """
        if self._service_update_callback:
            self._service_update_callback(
                self._service_arguments.id, self.get_formatted_results()
            )

    def cancel(self) -> None:
        """
        A method to cancel the current operation
        """
        raise NotImplementedError
