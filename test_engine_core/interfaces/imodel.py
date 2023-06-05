from abc import abstractmethod
from typing import Any, Tuple

from test_engine_core.interfaces.iplugin import IPlugin
from test_engine_core.plugins.enums.model_plugin_type import ModelPluginType


class IModel(IPlugin):
    """
    The IModel interface specifies methods for different supported model formats
    """

    @abstractmethod
    def __init__(self, model: Any) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def cleanup(self) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def setup(self) -> Tuple[bool, str]:
        pass  # pragma: no cover

    @abstractmethod
    def get_model(self) -> Any:
        pass  # pragma: no cover

    @abstractmethod
    def get_model_algorithm(self) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def get_model_plugin_type(self) -> ModelPluginType:
        pass  # pragma: no cover

    @abstractmethod
    def is_supported(self) -> bool:
        pass  # pragma: no cover

    @abstractmethod
    def predict(self, data: Any, data_labels: Any) -> Any:
        pass  # pragma: no cover

    @abstractmethod
    def predict_proba(self, data: Any, data_labels: Any) -> Any:
        pass  # pragma: no cover

    @abstractmethod
    def score(self, data: Any, y_true: Any) -> Any:
        pass  # pragma: no cover
