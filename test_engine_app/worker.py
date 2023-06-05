import signal
import sys
from multiprocessing import Lock
from typing import Dict, List, Union

from test_engine_app.app_logger import AppLogger
from test_engine_app.config.environment_variables import EnvironmentVariables
from test_engine_app.enums.service_type import ServiceType
from test_engine_app.enums.task_type import TaskType
from test_engine_app.enums.worker_type import WorkerType
from test_engine_app.network.redis import Redis
from test_engine_app.network.redis_constants import (
    REDIS_STREAM_SERVICE_NAME,
    REDIS_STREAM_TASK_NAME,
)
from test_engine_app.processing.iworkerfunction import IWorkerFunction
from test_engine_app.processing.plugin_controller import PluginController
from test_engine_app.processing.task import Task
from test_engine_app.processing.validate_dataset import ValidateDataset
from test_engine_app.processing.validate_model import ValidateModel
from test_engine_app.utils.validation_checks import is_empty_string


class Worker:
    """
    Worker class runs in a multiprocessing context.
    Each process will trigger the run method and perform what it requires.
    There are 2 types of worker, process or service worker.
    Process worker will perform differently compared to service workers.

    Process worker will wait for new tasks from the redis stream and
    Service worker will perform queries on model, data, compatibility issues.
    """

    # Class Variables
    _running_item: Union[IWorkerFunction, None] = None
    _logger: AppLogger = AppLogger()
    _to_stop: bool = False
    _worker_name: str = ""
    _worker_type: Union[WorkerType, None] = None
    lock: Lock = Lock()

    @staticmethod
    def run_initializer() -> None:
        """
        A method to register a SIGINT signal
        """
        signal.signal(signal.SIGINT, Worker.trigger_signal_handler)

    @staticmethod
    def run(worker_type: WorkerType, worker_id: int) -> None:
        """
        A method to start off the process on getting new tasks or queries and return results

        Args:
            worker_type (WorkerType): Indicates the task/service this process should take on
            worker_id (int): Indicates the process number
        """
        try:
            # Define ConsumerName id
            Worker._worker_name = f"Worker{worker_id}"
            Worker._worker_type = worker_type

            # Setup logging and error manager
            Worker._logger.generate_logger()
            Redis.set_logger(Worker._logger)
            Worker._logger.raw_logger_instance.info(
                f"Running: {Worker._worker_name} ({Worker._worker_type})"
            )

            # Read .env for environment variables.
            Worker._logger.raw_logger_instance.debug("Reading environment variables")
            EnvironmentVariables()
            Worker._logger.raw_logger_instance.debug(
                EnvironmentVariables.print_environment_variables()
            )

            # Setup PluginController
            PluginController.set_logger(Worker._logger)
            PluginController.setup(EnvironmentVariables.get_core_modules_folder())

            # Check if this thread is process worker or service worker
            if Worker._worker_type is WorkerType.SERVICE:
                stream_name = REDIS_STREAM_SERVICE_NAME
            else:
                stream_name = REDIS_STREAM_TASK_NAME

            # Setup Redis Pub/Sub channels and Stream (New Tasks)
            Worker._setup_redis(stream_name)

            # Clear all pending items
            Worker._logger.raw_logger_instance.debug("Clear pending redis stream items")
            Worker._clear_pending_items()

            # Discover new items and process
            Worker._logger.raw_logger_instance.debug(
                "Discovering new redis stream items"
            )
            Worker._discover_new_items()

            # Wait for CTRL-C to quit.
            signal.pause()

        except Exception as error:
            # Set the running item
            Worker._set_running_item(None)

            # Base try-except to catch all possible leaked exception and log them.
            if Worker._logger.raw_logger_instance:
                Worker._logger.raw_logger_instance.error(
                    f"An exception has occurred: {str(error)}"
                )

        finally:
            # Trigger a SIGINT signal to shut down the process properly.
            # Terminate process when it reaches the end
            Worker.trigger_signal_handler(signal.SIGINT, 1)

    @staticmethod
    def trigger_signal_handler(signum, frame) -> None:
        """
        A method to handle the SIGINT and trigger shutdown for processes

        Args:
            signum (_type_): NotUsed
            frame (_type_): NotUsed
        """
        # Trigger stop processing
        Worker._to_stop = True

        # Cleanup Redis
        Redis.cleanup()

        # Terminate logger instance
        if Worker._logger.raw_logger_instance:
            Worker._logger.raw_logger_instance.info(
                f"Stopping: {Worker._worker_name} ({Worker._worker_type})"
            )

        if Worker._logger.logger_instance:
            Worker._logger.logger_instance.stop()

        if Worker._logger.error_logger_instance:
            Worker._logger.error_logger_instance.write_error_to_file()

        # Terminate the application with exit code 0
        sys.exit(0)

    @staticmethod
    def _clear_pending_items() -> None:
        """
        A helper method to clear pending tasks/services that are not fully computed.
        When tasks/services are not being acked and read from the queue, they are called pending tasks/services.
        In this method, we will get the number of pending tasks/services, run the pending tasks/services
        and respond with an error, send the message ack to clear the entry.
        """
        # Get the current pending items list
        pending_items_list = Redis.get_pending_items(Worker._process_redis_message)

        # Clean up all the pending items
        for count in range(len(pending_items_list)):
            Worker._logger.raw_logger_instance.debug(
                f"Clearing pending items - {count + 1}/{len(pending_items_list)}"
            )

            # Read the new pending item from the list
            # Get the pending item instance for processing
            if Worker._worker_type is WorkerType.SERVICE:
                # Service WorkerType
                message_id, message_arguments, validation_type = pending_items_list[
                    count
                ]
                if validation_type is ServiceType.VALIDATE_MODEL:
                    pending_item = ValidateModel(
                        message_id,
                        message_arguments,
                        EnvironmentVariables.get_validation_schemas_folder(),
                        TaskType.PENDING,
                    )
                else:
                    pending_item = ValidateDataset(
                        message_id,
                        message_arguments,
                        EnvironmentVariables.get_validation_schemas_folder(),
                        TaskType.PENDING,
                    )

                # Perform logging
                Worker._logger.raw_logger_instance.info(
                    f"Clearing service: "
                    f"message_id {message_id}, "
                    f"message_args {message_arguments}, "
                    f"validation_type {validation_type}"
                )
            else:
                # Process WorkerType
                message_id, message_arguments = pending_items_list[count]
                pending_item = Task(
                    message_id,
                    message_arguments,
                    EnvironmentVariables.get_validation_schemas_folder(),
                    TaskType.PENDING,
                )

                # Perform Logging
                Worker._logger.raw_logger_instance.info(
                    f"Clearing item: "
                    f"message_id - {message_id}, "
                    f"message_args - {message_arguments}"
                )

            # Process the pending item
            is_success, error_messages = pending_item.process()
            if is_success:
                # Item completed processing
                Worker._logger.raw_logger_instance.info(
                    f"Completed Processing: "
                    f"message_id - {message_id}, "
                    f"message_args - {message_arguments}"
                )
            else:
                # Item failed processing
                Worker._logger.raw_logger_instance.error(
                    f"Failed Processing: "
                    f"message_id - {message_id}, "
                    f"message_args - {message_arguments}, "
                    f"error_messages - {error_messages}"
                )

            # Send Task Response and Ack
            if Worker._send_update(
                pending_item.get_id(), pending_item.get_formatted_results()
            ):
                Worker._send_acknowledgement(message_id)
            else:
                # Failed to send item update. Do not send item acknowledgement
                pass

            # Perform item cleanup
            pending_item.cleanup()

    @staticmethod
    def _discover_new_items() -> None:
        """
        A helper method to discover new redis stream items
        In this method, we will get a new item, run the item and send the message ack to clear the entry.
        """
        # Indicate number of items to get from redis stream at one time
        # Indicate number of milliseconds to block each time when reading streams
        get_num_of_items = 1
        blocking_duration = 2000

        # Continuously get new items and generate results
        while not Worker._to_stop:
            # Request for new items to process
            new_items_list = Redis.get_new_items(
                Worker._process_redis_message,
                get_num_of_items,
                blocking_duration,
            )

            # Loop through the message information
            # Create a new item and process the item
            # Send the response through redis
            # Clean up the generated item
            for count in range(len(new_items_list)):
                # Store current running item
                Worker._set_running_item(None)

                # Read the new pending item from the list
                # Get the pending item instance for processing
                if Worker._worker_type is WorkerType.SERVICE:
                    # Service WorkerType
                    message_id, message_arguments, validation_type = new_items_list[
                        count
                    ]
                    Worker._logger.raw_logger_instance.info(
                        f"Processing new service: "
                        f"message_id {message_id}, "
                        f"message_args {message_arguments}, "
                        f"validation_type {validation_type}"
                    )
                    if validation_type == ServiceType.VALIDATE_MODEL:
                        # Validate_MODEL ServiceType
                        new_item = ValidateModel(
                            message_id,
                            message_arguments,
                            EnvironmentVariables.get_validation_schemas_folder(),
                            TaskType.NEW,
                        )
                    else:
                        # Validate_DATASET ServiceType
                        new_item = ValidateDataset(
                            message_id,
                            message_arguments,
                            EnvironmentVariables.get_validation_schemas_folder(),
                            TaskType.NEW,
                        )
                else:
                    # Process WorkerType
                    message_id, message_arguments = new_items_list[count]
                    Worker._logger.raw_logger_instance.info(
                        f"Processing new task: "
                        f"message_id - {message_id}, "
                        f"message_args - {message_arguments}"
                    )
                    new_item = Task(
                        message_id,
                        message_arguments,
                        EnvironmentVariables.get_validation_schemas_folder(),
                        TaskType.NEW,
                        Worker._send_update,
                    )

                # Store current running item
                Worker._set_running_item(new_item)

                # Process the new item
                is_success, error_messages = new_item.process()
                if is_success:
                    # Task completed processing
                    Worker._logger.raw_logger_instance.info(
                        f"Completed Processing: "
                        f"message_id - {message_id}, "
                        f"message_args - {message_arguments}"
                    )
                else:
                    # Task failed processing
                    Worker._logger.raw_logger_instance.error(
                        f"Failed Processing: "
                        f"message_id - {message_id}, "
                        f"message_args - {message_arguments}, "
                        f"error_messages - {error_messages}"
                    )

                # Send Task Response and Ack
                if Worker._send_update(
                    new_item.get_id(), new_item.get_formatted_results()
                ):
                    Worker._send_acknowledgement(message_id)
                else:
                    # Failed to send update. Do not send acknowledgement
                    pass

                # Perform cleanup
                new_item.cleanup()

                # Set running item
                Worker._set_running_item(None)

    @staticmethod
    def _get_running_item() -> Union[IWorkerFunction, None]:
        """
        A helper method to return the running item

        Returns:
            running_item (Union[IWorkerFunction, None]): An instance of IWorkerFunction or None
        """
        with Worker.lock:
            # Returns the current running item
            return Worker._running_item

    @staticmethod
    def _process_redis_message(response_list: List) -> List:
        """
        A callback method to perform processing on messages from redis stream

        Args:
            response_list (List): The list that contains response from the redis stream

        Returns:
            List: A list of items after processing the messages
        """
        new_list = list()

        if Worker._worker_type is WorkerType.SERVICE:
            is_validate_dataset = response_list[0][1][0][1].get("validateDataset", None)
            is_validate_model = response_list[0][1][0][1].get("validateModel", None)

            # Get the message id and the arguments from the message information
            for count in range(len(response_list[0][1])):
                if response_list[0][0] == REDIS_STREAM_SERVICE_NAME:
                    message_id, message_dict = response_list[0][1][count]
                    if is_validate_dataset:
                        Worker._logger.raw_logger_instance.info(
                            "New message is received for validateDataset"
                        )
                        new_list.append(
                            (
                                message_id,
                                message_dict["validateDataset"],
                                ServiceType.VALIDATE_DATASET,
                            )
                        )
                    elif is_validate_model:
                        Worker._logger.raw_logger_instance.info(
                            "New message is received for validateModel"
                        )
                        new_list.append(
                            (
                                message_id,
                                message_dict["validateModel"],
                                ServiceType.VALIDATE_MODEL,
                            )
                        )
                    else:
                        Worker._logger.raw_logger_instance.warning(
                            f"Unknown message from {REDIS_STREAM_SERVICE_NAME}: {message_id}, {message_dict}"
                        )
                else:
                    Worker._logger.raw_logger_instance.warning(
                        f"New message is not from {REDIS_STREAM_SERVICE_NAME}"
                    )
        else:
            # Get the message id and the task arguments from the message information
            for count in range(len(response_list[0][1])):
                if response_list[0][0] == REDIS_STREAM_TASK_NAME:
                    message_id, message_dict = response_list[0][1][count]
                    new_list.append((message_id, message_dict["task"]))
                else:
                    Worker._logger.raw_logger_instance.warning(
                        f"New message is not from {REDIS_STREAM_TASK_NAME}"
                    )

        return new_list

    @staticmethod
    def _process_task_stop_callback(message: Dict) -> None:
        """
        A callback function to process task stop message

        Args:
            message (Dict): A pubsub message indicating the message id
        """
        item_id = message.get("data", None)
        Worker._logger.raw_logger_instance.info(
            f"Received request to stop task: {item_id}"
        )

        if not is_empty_string(item_id):
            running_item = Worker._get_running_item()
            if running_item:
                if item_id == running_item.get_id():
                    # This is the item that is running now. Cancel this item.
                    running_item.cancel()
                else:
                    # Running a different item
                    Worker._logger.raw_logger_instance.warning(
                        "Task not stopped: Running different item"
                    )
            else:
                # No running item
                Worker._logger.raw_logger_instance.warning(
                    "Task not stopped: No running task"
                )
        else:
            # Invalid item id
            Worker._logger.raw_logger_instance.error("Task not stopped: Empty task id")

    @staticmethod
    def _send_update(update_id: str, formatted_response: Dict) -> bool:
        """
        A helper method to send update using Redis

        Args:
            update_id (str): The id to be updated
            formatted_response (Dict): The formatted response

        Returns:
            bool: True if the update is sent, else False
        """
        # Check that the id is not empty
        if not is_empty_string(update_id):
            # Send Update
            if Redis.send_update(update_id, formatted_response):
                Worker._logger.raw_logger_instance.info(
                    f"Sent update - {update_id}:{formatted_response}"
                )
                return True
            else:
                Worker._logger.raw_logger_instance.warning(
                    f"Failed to send update - {update_id}:{formatted_response}"
                )
                return False
        else:
            Worker._logger.raw_logger_instance.warning(
                "Failed to send update - empty id"
            )
            return False

    @staticmethod
    def _send_acknowledgement(message_id: str) -> bool:
        """
        A helper method to send acknowledgement using Redis

        Args:
            message_id (str): The message id

        Returns:
            bool: True if the acknowledgement is sent, else False
        """
        # Check that the message_id is not empty
        if not is_empty_string(message_id):
            # Send Acknowledgement
            if Redis.send_acknowledgement(message_id):
                Worker._logger.raw_logger_instance.info(f"Completed - {message_id}")
                return True
            else:
                Worker._logger.raw_logger_instance.warning(
                    f"Failed to send message ack - {message_id}"
                )
                return False
        else:
            Worker._logger.raw_logger_instance.warning(
                "Failed to send acknowledgement - empty message id"
            )
            return False

    @staticmethod
    def _set_running_item(item: Union[IWorkerFunction, None]) -> None:
        """
        A helper method to update the running item

        Args:
            item (Union[IWorkerFunction, None]): An instance of IWorkerFunction or None
        """
        with Worker.lock:
            # Set the running item
            Worker._running_item = item

    @staticmethod
    def _setup_redis(stream_name: str) -> None:
        """
        A helper method to perform setup for redis.
        This includes setting up the pub/sub channels and the stream connections

        Args:
            stream_name (str): The redis stream name to be connected

        Raises:
            RuntimeError: Raise RuntimeError when Redis Pub/Sub channels failed to setup
            RuntimeError: Raise RuntimeError when Redis streams failed to setup
        """
        Worker._logger.raw_logger_instance.debug(
            f"Establishing redis connection to "
            f"{EnvironmentVariables.get_redis_server_hostname()}:"
            f"{EnvironmentVariables.get_redis_server_port()}"
        )

        # Establish redis connection
        Redis.setup(
            EnvironmentVariables.get_redis_server_hostname(),
            EnvironmentVariables.get_redis_server_port(),
        )

        # Setup pub/sub channels
        if Worker._worker_type is WorkerType.PROCESS:
            is_success = Redis.connect_to_pubsub(
                **{
                    "TASK_CANCEL": Worker._process_task_stop_callback,
                    "ALGO_INSTALL": PluginController.process_algorithm_install_callback,
                    "ALGO_UPDATE": PluginController.process_algorithm_update_callback,
                    "ALGO_DELETE": PluginController.process_algorithm_delete_callback,
                }
            )
            if is_success:
                Worker._logger.raw_logger_instance.debug(
                    "Redis Pub/Sub channels setup successfully"
                )
            else:
                # Error setting up redis.
                Worker._logger.raw_logger_instance.error(
                    "Redis Pub/Sub channels failed to setup"
                )
                raise RuntimeError("Redis Pub/Sub channels failed to setup")
        else:
            pass  # Other worker type do not need pubsub connection

        # Setup stream connection
        is_success, error_message = Redis.connect_to_stream(
            EnvironmentVariables.get_redis_consumer_group(),
            Worker._worker_name,
            stream_name,
        )
        if is_success:
            Worker._logger.raw_logger_instance.debug("Redis Streams setup successfully")
        else:
            # Error setting up redis.
            Worker._logger.raw_logger_instance.error(
                f"Redis Streams failed to setup: {error_message}"
            )
            raise RuntimeError(f"Redis Streams failed to setup: {error_message}")
