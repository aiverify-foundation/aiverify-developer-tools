from __future__ import annotations

import logging
from dataclasses import dataclass
from logging import Logger
from typing import Union

from test_engine_core.logging.error_manager import ErrorManager
from test_engine_core.logging.log_manager import LogManager
from test_engine_core.utils.generate_uuid import generate_uuid


@dataclass
class AppLogger:
    """
    AppLogger class create loggers for logging application and error messages
    """

    log_id: str

    # AppLogger
    logger_instance: Union[LogManager, None]
    raw_logger_instance: Union[Logger, None]
    log_filepath: str

    # Error AppLogger
    error_logger_instance: Union[ErrorManager, None]
    error_filepath: str

    def __init__(self):
        self.logger_instance = None
        self.raw_logger_instance = None
        self.log_filepath = ""

        self.error_logger_instance = None
        self.error_filepath = ""

    def generate_logger(self) -> None:
        """
        A method to generate uuid, logger and error logger for application
        """
        self.log_id = generate_uuid()

        # Setup AppLogger
        self.logger_instance = LogManager()
        self.logger_instance.create_logger(self.log_id)
        self.logger_instance.update_log_level("debug")
        self.raw_logger_instance = self.logger_instance.get_logger()
        self.log_filepath = self.logger_instance.get_log_filepath()

        # Setup Error Logger
        self.error_logger_instance = ErrorManager()
        self.error_logger_instance.create_error_manager(self.log_id)
        self.error_filepath = self.error_logger_instance.get_error_filepath()

    def generate_task_logger(self, task_id: str) -> None:
        """
        A method to generate uuid, logger and error logger for tasks

        Args:
            task_id (str): Task ID
        """
        self.log_id = task_id

        # Setup Task Logger
        self.logger_instance = LogManager()
        self.logger_instance.create_logger(self.log_id)
        self.raw_logger_instance = self.logger_instance.get_logger()
        self.log_filepath = self.logger_instance.get_log_filepath()

        # Setup Error Logger
        self.error_logger_instance = ErrorManager()
        self.error_logger_instance.create_error_manager(self.log_id)
        self.error_filepath = self.error_logger_instance.get_error_filepath()

    @staticmethod
    def add_to_log(app_logger: AppLogger, log_level: int, log_message: str) -> None:
        """
        A helper method to log messages to store events occurred

        Args:
            app_logger (AppLogger): The app logger instance for the message to be logged to
            log_level (int): The log level of the message
            log_message (str): The log message
        """
        if app_logger.raw_logger_instance:
            if log_level is logging.DEBUG:
                app_logger.raw_logger_instance.debug(log_message)

            elif log_level is logging.INFO:
                app_logger.raw_logger_instance.info(log_message)

            elif log_level is logging.WARNING:
                app_logger.raw_logger_instance.warning(log_message)

            elif log_level is logging.ERROR:
                app_logger.raw_logger_instance.error(log_message)

            elif log_level is logging.CRITICAL:
                app_logger.raw_logger_instance.critical(log_message)

            else:
                pass  # Invalid log level

        else:
            pass  # No log instance

    @staticmethod
    def add_error_to_log(
        app_logger: AppLogger,
        category: str,
        code: str,
        description: str,
        severity: str,
        origin: str,
        component: str,
    ):
        """
        A helper method to log messages to store error events occurred

        Args:
            app_logger (AppLogger): The app logger instance for the message to be logged to
            category (str): The error category
            code (str): The error code
            description (str): The error description
            severity (str): The error severity
            origin (str): The error origin
            component (str): The error component
        """
        if app_logger.error_logger_instance:
            app_logger.error_logger_instance.add_error_to_list(
                category, code, description, severity, origin, component
            )
        else:
            pass  # No log instance
