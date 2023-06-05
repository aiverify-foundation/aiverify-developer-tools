import json
import signal
import sys
from multiprocessing import Process
from typing import Union

from aiohttp import web

from test_engine_app.app_logger import AppLogger
from test_engine_app.config.environment_variables import EnvironmentVariables
from test_engine_app.enums.worker_type import WorkerType
from test_engine_app.utils.requirements_checks import is_package_supported


class RequirementsCheckApi:
    """
    RequirementsCheckApi class runs in a multiprocessing context.
    The run method and perform the generation of api server and the class handles the
    end point triggers using aiohttp.
    """

    # Class Variables
    _routes = web.RouteTableDef()
    _logger: AppLogger = AppLogger()
    _api_server_process = 0
    _worker_name: str = ""
    _worker_type: Union[WorkerType, None] = None

    @_routes.get("/requirements/client")
    async def requirements_check(request: web.Request) -> str:
        """
        A method for http endpoint to handle requirements check request

        Args:
            request: contains the http call data

        Raises:
            json.JSONDecodeError: Raise exception when the returned string of pip list isn't in json format

        Returns:
            str: result of each of the requirements received, in json array.
        """
        result = list()
        try:
            input_json = await request.json()
            for item in input_json:
                package_requirement = item["requirement"]
                is_package_supported_result = is_package_supported(package_requirement)
                package_result_json = {
                    "requirement": package_requirement,
                    "result": is_package_supported_result[0],
                    "comment": is_package_supported_result[1],
                }
                result.append(package_result_json)
        except json.decoder.JSONDecodeError as e:
            error_msg = f"JSONDecodeError caught: {e}"
            return web.Response(text=error_msg)
        except Exception as ex:
            error_msg = f"Exception caught: {ex}"
            return web.Response(text=error_msg)
        return web.Response(text=str(result), content_type="application/json")

    @staticmethod
    def run_initializer() -> None:
        """
        A method to register a SIGINT signal
        """
        signal.signal(signal.SIGINT, RequirementsCheckApi.trigger_signal_handler)

    @staticmethod
    def run(worker_type: WorkerType, worker_id: int) -> None:
        """
        This method generates the api server
        """

        try:
            RequirementsCheckApi.run_initializer()

            RequirementsCheckApi._worker_name = f"Worker{worker_id}"
            RequirementsCheckApi._worker_type = worker_type

            # Setup logging and error manager
            RequirementsCheckApi._logger.generate_logger()
            RequirementsCheckApi._logger.raw_logger_instance.info(
                f"Stopping: {RequirementsCheckApi._worker_name} ({RequirementsCheckApi._worker_type})"
            )

            # Read .env for environment variables.
            RequirementsCheckApi._logger.raw_logger_instance.debug(
                "Reading environment variables"
            )
            EnvironmentVariables()
            RequirementsCheckApi._logger.raw_logger_instance.debug(
                EnvironmentVariables.print_environment_variables()
            )

            RequirementsCheckApi._api_server_process = Process(
                target=RequirementsCheckApi.create_api_server
            )
            RequirementsCheckApi._api_server_process.start()

            # Wait for CTRL-C to quit.
            signal.pause()

        except Exception as error:
            # Base try-except to catch all possible leaked exception and log them.
            if RequirementsCheckApi._logger.raw_logger_instance:
                RequirementsCheckApi._logger.raw_logger_instance.error(
                    f"An exception has occurred: {str(error)}"
                )

        finally:
            # Trigger a SIGINT signal to shut down the process properly.
            # Terminate process when it reaches the end
            RequirementsCheckApi.trigger_signal_handler(signal.SIGINT, 1)

    @staticmethod
    def create_api_server():
        """
        A method to create api server instance
        """
        # Create API server
        app = web.Application()
        app.add_routes(RequirementsCheckApi._routes)
        web.run_app(app, port=EnvironmentVariables.get_api_server_port())

    @staticmethod
    def trigger_signal_handler(signum, frame) -> None:
        """
        A method to handle the SIGINT and trigger shutdown for processes

        Args:
            signum (_type_): NotUsed
            frame (_type_): NotUsed
        """
        # Terminate logger instance
        if RequirementsCheckApi._logger.raw_logger_instance:
            RequirementsCheckApi._logger.raw_logger_instance.info(
                f"Stopping: {RequirementsCheckApi._worker_name} ({RequirementsCheckApi._worker_type})"
            )

        if RequirementsCheckApi._logger.logger_instance:
            RequirementsCheckApi._logger.logger_instance.stop()

        if RequirementsCheckApi._logger.error_logger_instance:
            RequirementsCheckApi._logger.error_logger_instance.write_error_to_file()

        if RequirementsCheckApi._api_server_process:
            RequirementsCheckApi._api_server_process.terminate()

        # Terminate the application with exit code 0
        sys.exit(0)
