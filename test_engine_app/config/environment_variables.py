import os
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv

from test_engine_app.utils.validation_checks import is_empty_string


class EnvironmentVariables:
    """
    EnvironmentVariables class focuses on getting external environment variables that may affect how the program runs.
    """

    # Class Variables
    _default_env_file: str = ".env"
    _core_modules_folder: str = str(Path().resolve() / "core_modules")
    _validation_schemas_folder: str = str(Path().resolve() / "validation_schemas")
    _redis_consumer_group: str = "MyGroup"
    _redis_server_hostname: str = "localhost"
    _redis_server_port: int = 6379
    _api_server_port: int = 8080

    @staticmethod
    def reset() -> None:
        """
        A static method to be called by pytest to clear the instance
        """
        EnvironmentVariables._core_modules_folder = str(
            Path().resolve() / "core_modules"
        )
        EnvironmentVariables._validation_schemas_folder = str(
            Path().resolve() / "validation_schemas"
        )
        EnvironmentVariables._redis_consumer_group = "MyGroup"
        EnvironmentVariables._redis_server_hostname = "localhost"
        EnvironmentVariables._redis_server_port = 6379
        EnvironmentVariables._api_server_port = 8080

    def __init__(self):
        """
        Initialisation of Environment Variables
        """
        try:
            # Check if the '.env' file exists
            if Path.exists(Path(self._default_env_file)):
                # Read the environment variable file and load the variables
                load_dotenv(dotenv_path=self._default_env_file, override=True)

                # Save the files obtained from the file
                core_modules_folder = os.getenv(
                    "CORE_MODULES_FOLDER", str(Path().resolve() / "core_modules")
                )
                validation_schemas_folder = os.getenv(
                    "VALIDATION_SCHEMAS_FOLDER",
                    str(Path().resolve() / "validation_schemas"),
                )
                consumer_group = os.getenv("REDIS_CONSUMER_GROUP", "MyGroup")
                hostname = os.getenv("REDIS_SERVER_HOSTNAME", "localhost")
                server_port = int(os.getenv("REDIS_SERVER_PORT", 6379))
                api_server_port = int(os.getenv("API_SERVER_PORT", 8080))

                error_count, error_message = EnvironmentVariables._validate_data(
                    core_modules_folder,
                    validation_schemas_folder,
                    consumer_group,
                    hostname,
                    server_port,
                    api_server_port,
                )

                if error_count == 0:
                    EnvironmentVariables._core_modules_folder = core_modules_folder
                    EnvironmentVariables._validation_schemas_folder = (
                        validation_schemas_folder
                    )
                    EnvironmentVariables._redis_consumer_group = consumer_group
                    EnvironmentVariables._redis_server_hostname = hostname
                    EnvironmentVariables._redis_server_port = server_port
                    EnvironmentVariables._api_server_port = api_server_port
                else:
                    # Validation failed. Use defaults.
                    pass

        except ValueError:
            # ValueError exception. Use defaults.
            pass

    @staticmethod
    def _validate_data(
        core_modules_folder: str,
        validation_schemas_folder: str,
        consumer_group: str,
        hostname: str,
        server_port: int,
        api_server_port: int,
    ) -> Tuple[int, str]:
        """
        A helper method to perform data validation on the different arguments.

        Args:
            core_modules_folder (Path): Core Modules folder
            validation_schemas_folder (Path): Validation Schemas folder
            consumer_group (str): Redis Stream ConsumerGroup
            hostname (str): Redis Hostname
            server_port (int): Redis Server Port
            api_server_port (int): API Server Port
        Returns:
            Tuple[int, str]: error count and the error message.
        """
        error_count: int = 0
        error_message: str = ""

        # Core Modules folder
        if not Path(core_modules_folder).is_dir():
            error_count += 1
            error_message += "Core Modules folder is not a directory;"

        # Validation Schemas folder
        if not Path(validation_schemas_folder).is_dir():
            error_count += 1
            error_message += "Validation Schemas folder is not a directory;"

        # ConsumerGroup
        if is_empty_string(consumer_group):
            error_count += 1
            error_message += "Consumer Group is empty string;"

        # Hostname
        if is_empty_string(hostname):
            error_count += 1
            error_message += "Host name is empty string;"

        # Port number
        if server_port < 1 or server_port > 65535:
            error_count += 1
            error_message += "Server Port outside range;"

        # API Port number
        if api_server_port < 1 or api_server_port > 65535:
            error_count += 1
            error_message += "API Server Port outside range;"

        return error_count, error_message

    @staticmethod
    def print_environment_variables() -> str:
        """
        A method to return the string of environment variables for logging

        Returns:
            str: string formatted for printing the environment variables
        """
        return_str: str = "\nEnvironment Variables:\n"
        return_str += (
            f"CORE_MODULES_FOLDER: {EnvironmentVariables._core_modules_folder}\n"
        )
        return_str += f"VALIDATION_SCHEMAS_FOLDER: {EnvironmentVariables._validation_schemas_folder}\n"
        return_str += (
            f"REDIS_CONSUMER_GROUP: {EnvironmentVariables._redis_consumer_group}\n"
        )
        return_str += (
            f"REDIS_SERVER_HOSTNAME: {EnvironmentVariables._redis_server_hostname}\n"
        )
        return_str += f"REDIS_SERVER_PORT: {EnvironmentVariables._redis_server_port}\n"
        return_str += f"API_SERVER_PORT: {EnvironmentVariables._api_server_port}\n"

        return return_str

    @staticmethod
    def get_core_modules_folder() -> str:
        """
        A method to return the core modules folder that consists of data, models and serializers

        Returns:
            str: The string containing the core modules folder
        """
        return str(EnvironmentVariables._core_modules_folder)

    @staticmethod
    def get_validation_schemas_folder() -> str:
        """
        A method to return the validation schemas folder that consists of test engine task schema and others

        Returns:
            str: The string containing the validation schemas folder
        """
        return str(EnvironmentVariables._validation_schemas_folder)

    @staticmethod
    def get_redis_consumer_group() -> str:
        """
        A method to return the redis stream consumer group

        Returns:
            str: The string containing the stream consumer group name
        """
        return EnvironmentVariables._redis_consumer_group

    @staticmethod
    def get_redis_server_hostname() -> str:
        """
        A method to return the redis server host name

        Returns:
            str: The string containing the redis server host name
        """
        return EnvironmentVariables._redis_server_hostname

    @staticmethod
    def get_redis_server_port() -> int:
        """
        A method to return the redis server port

        Returns:
            int: redis server port number
        """
        return int(EnvironmentVariables._redis_server_port)

    @staticmethod
    def get_api_server_port() -> int:
        """
        A method to return the api server port

        Returns:
            int: api server port number
        """
        return int(EnvironmentVariables._api_server_port)
