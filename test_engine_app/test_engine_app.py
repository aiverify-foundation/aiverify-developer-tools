import os
import signal
import sys
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context

from test_engine_core.cli import version_msg

from test_engine_app import __version__
from test_engine_app.api.requirements_check_api import RequirementsCheckApi
from test_engine_app.app_logger import AppLogger
from test_engine_app.enums.worker_type import WorkerType
from test_engine_app.worker import Worker


class TestEngineApp:
    """
    The TestEngineApp class will initialize the methods required to run the TestEngineApp application.
    It will launch multiple processes which reads the environment variables, and process tasks
    It will detect SIGINT and performs a graceful shutdown of the application.
    """

    # Class Variable
    _logger: AppLogger = AppLogger()

    @staticmethod
    def version_msg() -> str:
        """
        Return the test engine app version, location and Python powering it.

        Returns:
            str: version string
        """
        python_version = sys.version
        location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return (
            f"Test Engine App - {__version__} from {location} (Python {python_version})"
        )

    def __init__(self):
        """
        Initialisation for Test Engine App
        """
        # Setup logger
        TestEngineApp._logger.generate_logger()

        # Get the number of processes that can be launched
        self._min_number_of_processes = 3
        self._available_number_of_processes = os.cpu_count()
        self._executor = ProcessPoolExecutor(
            mp_context=get_context("spawn"),
            max_workers=self._available_number_of_processes,
            initializer=Worker.run_initializer,
        )

        # Create a new list for worker futures
        self._worker_futures = list()

    def run(self) -> None:
        """
        A method to run Test Engine App
        """
        # Log test engine core and app version message
        TestEngineApp._logger.raw_logger_instance.info(TestEngineApp.version_msg())
        TestEngineApp._logger.raw_logger_instance.info(version_msg())

        # Check the available number of cores and launch the processes
        if self._available_number_of_processes < self._min_number_of_processes:
            TestEngineApp._logger.raw_logger_instance.error(
                f"Failed to start test engine. Insufficient number of cores available: "
                f"{self._available_number_of_processes}/{self._min_number_of_processes}"
            )

        else:
            # Define the number of service and process workers
            num_of_api_workers = 1
            num_of_service_workers = 1
            num_of_process_workers = (
                self._available_number_of_processes
                - num_of_service_workers
                - num_of_api_workers
            )

            TestEngineApp._logger.raw_logger_instance.info(
                f"Running Test Engine App: "
                f"LogID ({TestEngineApp._logger.log_id}), "
                f"API Workers ({num_of_api_workers}), "
                f"Service Workers ({num_of_service_workers}), "
                f"Process Workers ({num_of_process_workers})"
            )

            # Submit tasks to the ProcessPool
            worker_count = 0
            for count in range(num_of_api_workers):
                worker_count += 1
                self._worker_futures.append(
                    self._executor.submit(
                        RequirementsCheckApi.run, WorkerType.API_SERVER, worker_count
                    )
                )
            for count in range(num_of_process_workers):
                worker_count += 1
                self._worker_futures.append(
                    self._executor.submit(Worker.run, WorkerType.PROCESS, worker_count)
                )
            for count in range(num_of_service_workers):
                worker_count += 1
                self._worker_futures.append(
                    self._executor.submit(Worker.run, WorkerType.SERVICE, worker_count)
                )

            # Wait for CTRL-C to quit.
            signal.signal(signal.SIGINT, self.sigint_handler)
            TestEngineApp._logger.raw_logger_instance.info(
                "Press Ctrl+C to terminate Test Engine App"
            )
            signal.pause()

    def sigint_handler(self, signum, frame) -> None:
        """
        A method to handle the SIGINT and trigger shutdown

        Args:
            signum (_type_): NotUsed
            frame (_type_): NotUsed
        """
        TestEngineApp._logger.raw_logger_instance.info("Stopping Test Engine App...")

        # Check the future list and call cancel
        for future in self._worker_futures:
            future.cancel()

        # Shutdown the executor
        self._executor.shutdown()

        # Terminate logger instance
        if TestEngineApp._logger.logger_instance:
            TestEngineApp._logger.logger_instance.stop()

        # Terminate the application with exit code 0
        sys.exit(0)
