from abc import abstractmethod
from typing import Any, Tuple, Dict

from test_engine_core.interfaces.iplugin import IPlugin
from test_engine_core.plugins.enums.data_plugin_type import DataPluginType


class IData(IPlugin):
    """
    The IData interface specifies methods for different supported data formats
    """

    @abstractmethod
    def __init__(self, data: Any) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def setup(self) -> Tuple[bool, str]:
        pass  # pragma: no cover

    @abstractmethod
    def get_data(self) -> Any:
        pass  # pragma: no cover

    @abstractmethod
    def get_data_plugin_type(self) -> DataPluginType:
        pass  # pragma: no cover

    @abstractmethod
    def is_supported(self) -> bool:
        pass  # pragma: no cover

    @abstractmethod
    def keep_ground_truth(self, ground_truth: str) -> bool:
        pass  # pragma: no cover

    @abstractmethod
    def read_labels(self) -> Dict:
        pass  # pragma: no cover

    @abstractmethod
    def remove_ground_truth(self, ground_truth: str) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def validate(self) -> Tuple[bool, str]:
        pass  # pragma: no cover
