from typing import Callable, Dict, Tuple, Union

from test_engine_core.interfaces.imodel import IModel
from test_engine_core.plugins.enums.model_plugin_type import ModelPluginType
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
from test_engine_app.processing.validate_model_argument import ValidateModelArgument


class ValidateModel(IWorkerFunction):
    """
    ValidateModel class focuses on storing information and allows data processing and
    printing results of model validation
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
        self._service_arguments: ValidateModelArgument = ValidateModelArgument(
            validation_schemas_folder
        )

        # Service metadata and logging
        self._logger: AppLogger = AppLogger()
        self._metadata: ServiceMetadata = ServiceMetadata()

        # Service data
        self._model_instance: Union[IModel, None] = None

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
        return ServiceFormatter.format_model_validation_response(
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
                f"Processing model validation service: "
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
                    "validate_model.py",
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
                "validate_model.py",
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
                self._model_instance,
                self._serializer_instance,
                self._error_message,
            ) = PluginController.get_plugin_instance(
                PluginType.MODEL,
                **{
                    "mode": self._service_arguments.model_mode,
                    "filename": self._service_arguments.model_path,
                    "api_schema": self._service_arguments.api_schema,
                    "api_config": self._service_arguments.api_config,
                },
            )

            if not self._model_instance:
                error_messages = self._error_message
                self._logger.raw_logger_instance.warning(
                    f"Service Terminated: {error_messages}"
                )
                self._logger.error_logger_instance.add_error_to_list(
                    "MOD",
                    "WMODx00002",
                    f"{error_messages}",
                    "Warning",
                    "System",
                    "validate_model.py",
                )
                is_success = True
                self._set_file_invalid()

            else:
                # Write serializer type and model format to results
                self._set_service_results(
                    self._model_instance.get_model_plugin_type(),
                    self._serializer_instance.get_serializer_plugin_type(),
                )
                is_success = True
                self._set_file_valid()

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
                f"{error_messages}",
                "Warning",
                "System",
                "validate_model.py",
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
            "validate_model.py",
        )

        # Set current service as failure
        self._set_service_failure()

        return True, ""

    def _set_service_results(
        self, model_format: ModelPluginType, serializer_type: SerializerPluginType
    ) -> None:
        """
        A helper method to update the new service results

        Args:
            model_format (ModelPluginType): Name of the model format
            serializer_type (SerializerPluginType): Name of the serializer type
        """

        self._logger.raw_logger_instance.info(
            f"Model format: {model_format.name} and serializer type: {serializer_type.name} writing to metadata..."
        )

        self._metadata.serializer_type = serializer_type
        self._metadata.model_format = model_format

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
