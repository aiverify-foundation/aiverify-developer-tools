import logging
from time import sleep
from typing import Callable, Dict, List, Tuple, Union

import redis
from test_engine_core.network.redis.redis_pubsub import RedisPubSub
from test_engine_core.network.redis.redis_stream import RedisStream

from test_engine_app.app_logger import AppLogger
from test_engine_app.network.redis_constants import (
    REDIS_PUBSUB_ALERT_NAME,
    REDIS_PUBSUB_ALGO_DELETE_NAME,
    REDIS_PUBSUB_ALGO_INSTALL_NAME,
    REDIS_PUBSUB_ALGO_UPDATE_NAME,
    REDIS_PUBSUB_TASK_CANCEL_NAME,
)


class Redis:
    """
    Redis class will establish the connection to redis, and be a middleman in sending the request
    and getting the response.
    """

    # Class Variables
    _logger: Union[AppLogger, None] = None
    _server_hostname: Union[str, None] = None
    _server_hostport: Union[int, None] = None
    _alert_pubsub: Union[RedisPubSub, None] = None
    _algo_install_pubsub: Union[RedisPubSub, None] = None
    _algo_update_pubsub: Union[RedisPubSub, None] = None
    _algo_delete_pubsub: Union[RedisPubSub, None] = None
    _task_cancel_pubsub: Union[RedisPubSub, None] = None
    _stream_listener: Union[RedisStream, None] = None

    @staticmethod
    def setup(hostname: str, port: int) -> None:
        """
        A method to set the hostname and port number

        Args:
            hostname (str): The redis server hostname
            port (int): The redis server port number
        """
        Redis._server_hostname = hostname
        Redis._server_hostport = port

    @staticmethod
    def set_logger(logger: AppLogger) -> None:
        """
        A method to set up the logger instance for logging

        Args:
            logger (AppLogger): The logger instance
        """
        Redis._logger = logger

    @staticmethod
    def cleanup() -> None:
        """
        A method to clean up all the pubsub channels
        """
        if Redis._task_cancel_pubsub:
            Redis._task_cancel_pubsub.stop()

        if Redis._algo_install_pubsub:
            Redis._algo_install_pubsub.stop()

        if Redis._algo_update_pubsub:
            Redis._algo_update_pubsub.stop()

        if Redis._algo_delete_pubsub:
            Redis._algo_delete_pubsub.stop()

    @staticmethod
    def connect_to_stream(
        consumer_group: str,
        consumer_name: str,
        stream_name: str,
    ) -> Tuple[bool, str]:
        """
        A method to set up Redis Stream Listener

        Args:
            consumer_group (str): redis consumer group for stream
            consumer_name (str): redis consumer name for redis consumer group
            stream_name (str): redis stream name

        Raises:
            RuntimeError: Raises exception when unable to connect to redis server

        Returns:
            Tuple[bool, str]: True if set up successful else False and error message if set up failed.
        """
        try:
            Redis._stream_listener = RedisStream()
            is_success, error_message = Redis._stream_listener.setup(
                Redis._server_hostname,
                Redis._server_hostport,
                stream_name,
                consumer_group,
                consumer_name,
            )
            if is_success:
                AppLogger.add_to_log(
                    Redis._logger,
                    logging.INFO,
                    f"RedisStreamListener: {str(stream_name)} Connected",
                )
                return is_success, ""
            else:
                raise RuntimeError(
                    f"RedisStreamListener is not initialized: {error_message}"
                )

        except RuntimeError as exception:
            AppLogger.add_to_log(
                Redis._logger,
                logging.ERROR,
                f"An exception has occurred: {str(exception)}",
            )
            AppLogger.add_error_to_log(
                Redis._logger,
                "SYS",
                "CSYSx00012",
                f"An exception has occurred: {str(exception)}",
                "Critical",
                "System",
                "redis.py",
            )
            return False, str(exception)

    @staticmethod
    def connect_to_pubsub(**kwargs) -> bool:
        """
        A method to set up Redis Pubsub
        This includes the alert channel, algo install/update/delete and task cancel channels.

        Returns:
            bool: True if set up successful else False if failed.
        """
        Redis._task_cancel_pubsub = Redis._subscribe_channel(
            REDIS_PUBSUB_TASK_CANCEL_NAME, kwargs["TASK_CANCEL"]
        )
        Redis._algo_install_pubsub = Redis._subscribe_channel(
            REDIS_PUBSUB_ALGO_INSTALL_NAME, kwargs["ALGO_INSTALL"]
        )
        Redis._algo_update_pubsub = Redis._subscribe_channel(
            REDIS_PUBSUB_ALGO_UPDATE_NAME, kwargs["ALGO_UPDATE"]
        )
        Redis._algo_delete_pubsub = Redis._subscribe_channel(
            REDIS_PUBSUB_ALGO_DELETE_NAME, kwargs["ALGO_DELETE"]
        )
        Redis._alert_pubsub = Redis._publish_channel(REDIS_PUBSUB_ALERT_NAME)

        if (
            Redis._task_cancel_pubsub
            and Redis._algo_install_pubsub
            and Redis._algo_update_pubsub
            and Redis._algo_delete_pubsub
            and Redis._alert_pubsub
        ):
            return True
        else:
            return False

    @staticmethod
    def get_algorithm_info(algorithm_id: str) -> Dict:
        """
        A method to return a dict of information related to the algorithm if found in algorithm registry

        Args:
            algorithm_id (str): The id of the algorithm stored in algorithm registry

        Raises:
            RuntimeError: Raise exception when stream listener is not initialized
            RuntimeError: Raise exception when encountered connection error

        Returns:
            Dict: A Dict of information if the algorithm is found or Empty Dict if algorithm is not found.
        """
        algorithm_info = dict()
        try:
            if Redis._stream_listener:
                # Read algorithm information from stream
                response = Redis._stream_listener.read_algorithm_registry(algorithm_id)
                if response and type(response) == dict:
                    algorithm_info = response

                return algorithm_info
            else:
                raise RuntimeError("RedisStreamListener is not initialized")

        except redis.exceptions.ConnectionError as error:
            raise RuntimeError(f"Encountered connection error: {str(error)}")

        except Exception as exception:
            AppLogger.add_to_log(
                Redis._logger,
                logging.ERROR,
                f"An exception has occurred: {str(exception)}",
            )
            AppLogger.add_error_to_log(
                Redis._logger,
                "SYS",
                "CSYSx00012",
                f"An exception has occurred: {str(exception)}",
                "Critical",
                "System",
                "redis.py",
            )
            return algorithm_info

    @staticmethod
    def get_new_items(
        callback_func: Callable,
        read_num_of_jobs: int = 1,
        blocking_duration_ms: Union[int, None] = None,
    ) -> List:
        """
        A method to return a list of new items for processing
        If there are no messages in the message queue, it will return None instead

        Args:
            callback_func (Callable): The function that will decide how to process before appending to the list
            read_num_of_jobs (int, optional): Number of messages to read from stream. Defaults to 1.
            blocking_duration_ms (Union[int, None], optional): Number of milliseconds for blocking call.
            Defaults to None.

        Raises:
            RuntimeError: Raise exception when stream listener is not initialized
            RuntimeError: Raise exception when encountered connection error

        Returns:
            List: A List of object if there is message or Empty List if no new messages.
        """
        new_items: List = list()
        try:
            if Redis._stream_listener:
                # Read new message from stream
                response_list = Redis._stream_listener.read_message(
                    read_num_of_jobs, blocking_duration_ms
                )
                if response_list and type(response_list) == list:
                    # Trigger callback to run this portion
                    # If list not empty, append the items to our list
                    result = callback_func(response_list)
                    if result:
                        new_items.extend(result)
                else:
                    # Unexpected response
                    pass

                return new_items
            else:
                raise RuntimeError("RedisStreamListener is not initialized")

        except redis.exceptions.ConnectionError as error:
            AppLogger.add_to_log(
                Redis._logger,
                logging.WARNING,
                "Sleep for 1 second before trying again.",
            )
            sleep(1)
            raise RuntimeError(f"Encountered connection error: {str(error)}")

        except Exception as exception:
            AppLogger.add_to_log(
                Redis._logger,
                logging.ERROR,
                f"An exception has occurred: {str(exception)}",
            )
            AppLogger.add_error_to_log(
                Redis._logger,
                "SYS",
                "CSYSx00012",
                f"An exception has occurred: {str(exception)}",
                "Critical",
                "System",
                "redis.py",
            )
            return new_items

    @staticmethod
    def get_pending_items(callback_func: Callable) -> List:
        """
        A method to return a list of pending items for processing
        If there are no messages in the message queue, it will return None instead

        Args:
            callback_func (Callable): The function that will decide how to process before appending to the list

        Raises:
            RuntimeError: Raise exception when stream listener is not initialized
            RuntimeError: Raise exception when encountered connection error

        Returns:
            List: A List of object if there is message or Empty List if no new messages.
        """
        new_items: List = list()
        try:
            if Redis._stream_listener:
                # Get the number of pending items
                num_of_pending_items = (
                    Redis._stream_listener.read_number_of_pending_messages()
                )

                # If there are no pending items, return empty list
                if num_of_pending_items > 0:
                    # If there are pending items, read all the pending items and store them in response_list.
                    # Validate the response list and append the required information and return the new_items.
                    response_list = Redis._stream_listener.read_pending_message(
                        num_of_pending_items
                    )
                    if response_list and type(response_list) == list:
                        # Trigger callback to run this portion
                        # If list not empty, append the items to our list
                        result = callback_func(response_list)
                        if result:
                            new_items.extend(result)
                    else:
                        pass  # Unexpected response
                else:
                    pass  # No pending items

                return new_items

            else:
                raise RuntimeError("RedisStreamListener is not initialized")

        except redis.exceptions.ConnectionError as error:
            raise RuntimeError(f"Encountered connection error: {str(error)}")

        except Exception as exception:
            AppLogger.add_to_log(
                Redis._logger,
                logging.ERROR,
                f"An exception has occurred: {str(exception)}",
            )
            AppLogger.add_error_to_log(
                Redis._logger,
                "SYS",
                "CSYSx00012",
                f"An exception has occurred: {str(exception)}",
                "Critical",
                "System",
                "redis.py",
            )
            return new_items

    @staticmethod
    def send_acknowledgement(message_id: str) -> bool:
        """
        A method to send acknowledgement

        Args:
            message_id (str): Message Id

        Raises:
            RuntimeError: Raise exception when stream listener is not initialized
            RuntimeError: Raise exception when encountered connection error

        Returns:
            bool: True if send success, else False
        """
        is_success: bool = False
        try:
            if Redis._stream_listener:
                return Redis._stream_listener.send_message_acknowledgement(message_id)
            else:
                raise RuntimeError("RedisStreamListener is not initialized")

        except redis.exceptions.ConnectionError as error:
            raise RuntimeError(f"Encountered connection error: {str(error)}")

        except Exception as exception:
            AppLogger.add_to_log(
                Redis._logger,
                logging.ERROR,
                f"An exception has occurred: {str(exception)}",
            )
            AppLogger.add_error_to_log(
                Redis._logger,
                "SYS",
                "CSYSx00012",
                f"An exception has occurred: {str(exception)}",
                "Critical",
                "System",
                "redis.py",
            )
            return is_success

    @staticmethod
    def send_update(update_id: str, response: Dict) -> bool:
        """
        A method to send update

        Args:
            update_id (str): ID for the item to be updated
            response (Dict): Response for the item to be updated

        Raises:
            RuntimeError: Raise exception when stream listener is not initialized
            RuntimeError: Raise exception when encountered connection error

        Returns:
            bool: True if send success, else False
        """
        is_success: bool = False
        try:
            if Redis._stream_listener:
                return Redis._stream_listener.send_update(update_id, response)
            else:
                raise RuntimeError("RedisStreamListener is not initialized")

        except redis.exceptions.ConnectionError as error:
            raise RuntimeError(f"Encountered connection error: {str(error)}")

        except Exception as exception:
            AppLogger.add_to_log(
                Redis._logger,
                logging.ERROR,
                f"An exception has occurred: {str(exception)}",
            )
            AppLogger.add_error_to_log(
                Redis._logger,
                "SYS",
                "CSYSx00012",
                f"An exception has occurred: {str(exception)}",
                "Critical",
                "System",
                "redis.py",
            )
            return is_success

    @staticmethod
    def _publish_channel(channel_name: str) -> Union[RedisPubSub, None]:
        """
        A helper method to publish to pub/sub redis channels

        Args:
            channel_name (str): The redis pubsub channel

        Raises:
            RuntimeError: Raises exception when unable to connect to redis server

        Returns:
            Union[RedisPubSub, None]: Returns RedisPubSub instance if successful else None
        """
        try:
            # Create a pubsub instance
            pubsub_instance = RedisPubSub()
            is_success, error_message = pubsub_instance.setup(
                Redis._server_hostname, Redis._server_hostport, channel_name
            )

            if is_success:
                return pubsub_instance
            else:
                raise RuntimeError(f"Pub/Sub Channel ({channel_name}): {error_message}")

        except RuntimeError as exception:
            AppLogger.add_to_log(
                Redis._logger,
                logging.ERROR,
                f"An exception has occurred: {str(exception)}",
            )
            AppLogger.add_error_to_log(
                Redis._logger,
                "SYS",
                "CSYSx00012",
                f"An exception has occurred: {str(exception)}",
                "Critical",
                "System",
                "redis.py",
            )
            return None

    @staticmethod
    def _subscribe_channel(
        channel_name: str, callback_function: Callable
    ) -> Union[RedisPubSub, None]:
        """
        A helper method to subscribe to pub/sub redis channels

        Args:
            channel_name (str): The redis pubsub channel
            callback_function (Callable): The callback function for the message to be delivered to

        Raises:
            RuntimeError: Raises exception when callback method not provided
            RuntimeError: Raises exception when unable to subscribe to redis channel
            RuntimeError: Raises exception when unable to connect to redis server

        Returns:
            Union[RedisPubSub, None]: Returns RedisPubSub instance if successful else None
        """
        try:
            # Check for callback function
            if not callback_function:
                raise RuntimeError(
                    f"Pub/Sub Channel ({channel_name}): No callback function provided."
                )

            # Create a pubsub instance
            pubsub_instance = RedisPubSub()
            is_success, error_message = pubsub_instance.setup(
                Redis._server_hostname, Redis._server_hostport, channel_name
            )

            if is_success:
                if pubsub_instance.subscribe(callback_function):
                    AppLogger.add_to_log(
                        Redis._logger,
                        logging.DEBUG,
                        f"Pub/Sub Channel ({channel_name}): Subscribed",
                    )
                    return pubsub_instance

                else:
                    raise RuntimeError(
                        f"Pub/Sub Channel ({channel_name}): Not Subscribed"
                    )

            else:
                raise RuntimeError(f"Pub/Sub Channel ({channel_name}): {error_message}")

        except RuntimeError as exception:
            AppLogger.add_to_log(
                Redis._logger,
                logging.ERROR,
                f"An exception has occurred: {str(exception)}",
            )
            AppLogger.add_error_to_log(
                Redis._logger,
                "SYS",
                "CSYSx00012",
                f"An exception has occurred: {str(exception)}",
                "Critical",
                "System",
                "redis.py",
            )
            return None
