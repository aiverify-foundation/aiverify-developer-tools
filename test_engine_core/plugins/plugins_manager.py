import glob
import importlib.util
import re
import sys
from importlib.machinery import ModuleSpec
from logging import Logger
from multiprocessing import Lock
from pathlib import Path
from types import ModuleType
from typing import Dict, Tuple, Union

from test_engine_core.interfaces.ialgorithm import IAlgorithm
from test_engine_core.interfaces.idata import IData
from test_engine_core.interfaces.imodel import IModel
from test_engine_core.interfaces.iserializer import ISerializer
from test_engine_core.plugins.algorithm_manager import AlgorithmManager
from test_engine_core.plugins.data_manager import DataManager
from test_engine_core.plugins.enums.model_mode_type import ModelModeType
from test_engine_core.plugins.enums.plugin_type import PluginType
from test_engine_core.plugins.model_manager import ModelManager


class PluginManager:
    """
    The PluginManager class provides functionality for discovering plugins and interacting with different plugins
    """

    # Variables
    _logger: Logger = None
    _plugins: Dict = {plugin_type.name: dict() for plugin_type in PluginType}
    lock: Lock = Lock()
    plugin_name: str = "Plugin"

    @staticmethod
    def set_logger(logger: Logger) -> None:
        """
        A method to set up the logger instance for logging

        Args:
            logger (Logger): The logger instance
        """
        # Set all the different managers to the logger to perform logging when in operation
        PluginManager._logger = logger
        DataManager.set_logger(logger)
        ModelManager.set_logger(logger)
        AlgorithmManager.set_logger(logger)

    @staticmethod
    def discover(
        discover_folder: str = str(Path().absolute() / "plugins"), tag_name: str = None
    ) -> None:
        """
        A method to discover possible plugins in the Discover folder indicated during setup phase

        Args:
            discover_folder (str, optional): A path to discover new plugins.
            Defaults to str(Path().absolute() / "plugins").
            tag_name (str, optional): A string to tag this name with the module found. Defaults to None
        """
        # Find python files in the given folder.
        discover_paths = [
            file for file in glob.glob(f"{discover_folder}/**/*.py", recursive=True)
        ]

        # Search through the discovered paths and create modules
        plugin_modules = dict()
        for plugin_path in discover_paths:
            # Add the plugin folder in case it uses relative path
            plugin_folder_path = str(Path(plugin_path).parent)
            sys.path.append(plugin_folder_path)

            try:
                # Remove files that have underscores (__filename__.py)
                module_name = re.sub("\\.py$", "", Path(plugin_path).name)
                if module_name.__contains__("__"):
                    continue

                # Import module with the module specification
                # Store modules in the dict
                module_spec = PluginManager._create_module_spec(
                    module_name, plugin_path
                )
                if not module_spec:
                    continue  # module spec is None

                module = PluginManager._import_module_from_spec(module_spec)
                if (
                    PluginManager.plugin_name in dir(module)
                    and module.Plugin.get_plugin_type() in PluginType
                ):
                    if tag_name:
                        plugin_modules.update({tag_name: module})
                    else:
                        plugin_modules.update({module_name: module})
                else:
                    pass  # Unexpected module or Invalid plugin type

            except Exception:
                pass  # Encountered an error while processing this py file; Continue next file

            finally:
                # Remove the plugin folder from sys search path
                sys.path.remove(plugin_folder_path)

        # Update list of plugin modules
        PluginManager._update_plugin_modules(plugin_modules)

    @staticmethod
    def get_instance(
        plugin_type: PluginType, **kwargs
    ) -> Union[
        Tuple[IData, ISerializer, str],
        Tuple[IModel, ISerializer, str],
        Tuple[IAlgorithm, None, str],
    ]:
        """
        A method to retrieve the instance of plugins that is identified

        Args:
            plugin_type (PluginType): The plugin type to be identified

        Returns:
            Union[Tuple[IData, ISerializer, str], Tuple[IModel, ISerializer, str], Tuple[IAlgorithm, None, str]]:
            Returns an instance of the identified type with its serializer and error messages
        """
        if plugin_type is PluginType.DATA:
            return PluginManager._get_data_serializer_instance(kwargs)

        elif plugin_type is PluginType.MODEL:
            return PluginManager._get_model_serializer_instance(kwargs)

        else:
            return PluginManager._get_algorithm_serializer_instance(kwargs)

    @staticmethod
    def get_printable_plugins() -> str:
        """
        A method to get a printable string of detected plugins

        Returns:
            str: A str of detected plugins
        """
        with PluginManager.lock:
            return str(PluginManager._plugins)

    @staticmethod
    def is_plugin_exists(plugin_type: PluginType, plugin_name: str) -> bool:
        """
        A method to return if the plugin exists in detected plugins

        Args:
            plugin_type (PluginType): The plugin type (e.g. Data, Model, Algorithm, Serializer)
            plugin_name (str): The plugin name to be removed

        Returns:
            bool: Returns True if found, False if not found
        """
        plugins = PluginManager._get_plugins_by_type(plugin_type)
        if plugin_name in plugins.keys():
            return True
        else:
            return False

    @staticmethod
    def remove_plugin(plugin_type: PluginType, plugin_name: str) -> bool:
        """
        A method to remove plugin from the detected plugins

        Args:
            plugin_type (PluginType): The plugin type (e.g. Data, Model, Algorithm, Serializer)
            plugin_name (str): The plugin name to be removed

        Returns:
            bool: True if the plugin is not in the detected plugins, False if still in the detected plugins
        """
        # Delete the plugin
        PluginManager._delete_plugins_by_type(plugin_type, plugin_name)

        # Verify that the plugin is deleted
        if not PluginManager.is_plugin_exists(plugin_type, plugin_name):
            # Plugin not in the detected list
            return True
        else:
            # Plugin still in the detected list
            return False

    @staticmethod
    def _get_data_serializer_instance(
        arguments: Dict,
    ) -> Tuple[IData, ISerializer, str]:
        """
        A helper method to retrieve the data and serializer instance from DataManager

        Args:
            arguments (Dict): The arguments to be passed to the DataManager to process

        Raises:
            RuntimeError: Failure to load the data from the provided filepath

        Returns:
            Tuple[IData, ISerializer, str]: A data instance if the data is supported by the system,
            the serializer instance that is used to deserialize the data and error messages.
        """
        # Pass the information to DataManager to process and return the detected data instance
        filename = arguments.get("filename", "")
        (
            is_success,
            data_instance,
            serializer_instance,
            error_message,
        ) = DataManager.read_data_file(
            filename,
            PluginManager._get_plugins_by_type(PluginType.DATA),
            PluginManager._get_plugins_by_type(PluginType.SERIALIZER),
        )

        if is_success:
            return data_instance, serializer_instance, error_message
        else:
            raise RuntimeError(
                f"Failed to load dataset(file): {filename} ({error_message})"
            )

    @staticmethod
    def _get_model_serializer_instance(
        arguments: Dict,
    ) -> Tuple[IModel, ISerializer, str]:
        """
        A helper method to retrieve the model and serializer instance from ModelManager

        Args:
            arguments (Dict): The arguments to be passed to the ModelManager to process

        Raises:
            RuntimeError: Failure to load the model from the provided filepath

        Returns:
            Tuple[IModel, ISerializer, str]: A model instance if the model is supported by the system,
            the serializer instance that is used to deserialize the model and error messages.
        """
        # Pass the information to ModelManager to process and return the detected model instance
        model_mode = arguments.get("mode", ModelModeType.UPLOAD)

        # Process differently if it is API, or UPLOAD.
        if model_mode is ModelModeType.API:
            api_schema = arguments.get("api_schema", dict())
            api_config = arguments.get("api_config", dict())
            (
                is_success,
                model_instance,
                serializer_instance,
                error_message,
            ) = ModelManager.read_model_api(
                api_schema,
                api_config,
                PluginManager._get_plugins_by_type(PluginType.MODEL),
            )

            if is_success:
                return model_instance, serializer_instance, error_message
            else:
                raise RuntimeError(
                    f"Failed to load model(api): {api_schema} | {api_config} ({error_message})"
                )

        else:
            filename = arguments.get("filename", "")
            (
                is_success,
                model_instance,
                serializer_instance,
                error_message,
            ) = ModelManager.read_model_file(
                filename,
                PluginManager._get_plugins_by_type(PluginType.MODEL),
                PluginManager._get_plugins_by_type(PluginType.SERIALIZER),
            )

            if is_success:
                return model_instance, serializer_instance, error_message
            else:
                raise RuntimeError(
                    f"Failed to load model(file): {filename} ({error_message})"
                )

    @staticmethod
    def _get_algorithm_serializer_instance(
        arguments: Dict,
    ) -> Tuple[IAlgorithm, None, str]:
        """
        A helper method to retrieve algorithm and serializer instance from AlgorithmManager

        Args:
            arguments (Dict): The arguments to be passed to the AlgorithmManager to process

        Raises:
            RuntimeError: Failure to load algorithm from the provided algorithm id

        Returns:
            Tuple[IAlgorithm, None, str]: An algorithm instance if the algorithm is supported by the system
        """
        # Pass the information to AlgorithmManager to process and return the detected algorithm instance
        is_success, algorithm_instance, error_message = AlgorithmManager.get_algorithm(
            PluginManager._get_plugins_by_type(PluginType.ALGORITHM), **arguments
        )
        if is_success:
            return algorithm_instance, None, error_message
        else:
            raise RuntimeError(
                f"Failed to load algorithm: {arguments} ({error_message})"
            )

    @staticmethod
    def _delete_plugins_by_type(plugin_type: PluginType, plugin_name: str) -> None:
        """
        A helper method to remove plugin from stored plugins

        Args:
            plugin_type (PluginType): The plugin type (e.g. Data, Model, Algorithm, Serializer)
            plugin_name (str): The plugin name to be removed
        """
        with PluginManager.lock:
            if plugin_name in PluginManager._plugins[plugin_type.name].keys():
                PluginManager._plugins[plugin_type.name].pop(plugin_name)

    @staticmethod
    def _get_plugins_by_type(plugin_type: PluginType) -> Dict:
        """
        A helper method to return plugins from stored plugins

        Args:
            plugin_type (PluginType): The plugin type (e.g. Data, Model, Algorithm, Serializer)

        Returns:
            Dict: The installed plugins under this plugin type
        """
        with PluginManager.lock:
            if plugin_type is PluginType.DATA:
                return PluginManager._plugins[PluginType.DATA.name]
            elif plugin_type is PluginType.MODEL:
                return PluginManager._plugins[PluginType.MODEL.name]
            elif plugin_type is PluginType.SERIALIZER:
                return PluginManager._plugins[PluginType.SERIALIZER.name]
            else:
                return PluginManager._plugins[PluginType.ALGORITHM.name]

    @staticmethod
    def _update_plugins_by_type(plugin_type: PluginType, plugin_dict: Dict) -> None:
        """
        A helper method to add/update plugin to stored plugins

        Args:
            plugin_type (PluginType): The plugin type (e.g. Data, Model, Algorithm, Serializer)
            plugin_dict (Dict): The dict that contains the (plugin_name: plugin_obj)
        """
        with PluginManager.lock:
            PluginManager._plugins[plugin_type.name].update(plugin_dict)

    @staticmethod
    def _create_module_spec(
        module_name: str, module_file_path: str
    ) -> Union[None, ModuleSpec]:
        """
        A helper method to create module specifications if it does not exist

        Args:
            module_name (str): Input module name to be imported
            module_file_path (str): Input module file path to be imported

        Returns:
            Union[None, ModuleSpec]: Generated module specifications for importing or error
        """
        try:
            module_spec = importlib.util.find_spec(module_name)
            if module_spec is None:
                # Create a module spec since it is not available
                module_spec = importlib.util.spec_from_file_location(
                    module_name, module_file_path
                )

            return module_spec

        except ValueError:
            # Unable to find spec from this file to create
            return None

    @staticmethod
    def _import_module_from_spec(module_spec: ModuleSpec) -> ModuleType:
        """
        A helper method to import python module using module specifications

        Args:
            module_spec (ModuleSpec): A generated module specifications for the module to be imported

        Returns:
            ModuleType: An imported module
        """
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

    @staticmethod
    def _update_plugin_modules(modules: Dict) -> None:
        """
        A helper method to update the plugin manager plugins directory with new-found plugins

        Args:
            modules (Dict): A dictionary of newly found plugins
        """
        for module_name, module in modules.items():
            # Get the module plugin type
            plugin_type = module.Plugin.get_plugin_type()

            # Check if this module exists in the pluginmanager plugins list.
            # Add plugin if the module does not exist.
            if module_name not in PluginManager._get_plugins_by_type(plugin_type):
                PluginManager._update_plugins_by_type(
                    plugin_type, {module_name: module}
                )
