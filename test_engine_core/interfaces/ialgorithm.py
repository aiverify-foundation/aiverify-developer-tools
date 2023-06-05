from abc import abstractmethod
from typing import Dict

from test_engine_core.interfaces.idata import IData
from test_engine_core.interfaces.imodel import IModel
from test_engine_core.interfaces.iplugin import IPlugin


class IAlgorithm(IPlugin):
    """
    The IAlgorithm interface specifies methods for different supported algorithms
    """

    @abstractmethod
    def __init__(
        self, data: IData, model: IModel, ground_truth: IData, **kwargs
    ) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def setup(self) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def get_progress(self) -> int:
        pass  # pragma: no cover

    @abstractmethod
    def get_results(self) -> Dict:
        pass  # pragma: no cover

    @abstractmethod
    def generate(self) -> None:
        pass  # pragma: no cover
