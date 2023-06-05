from dataclasses import dataclass
from typing import Union

from test_engine_core.plugins.enums.data_plugin_type import DataPluginType
from test_engine_core.plugins.enums.model_plugin_type import ModelPluginType
from test_engine_core.plugins.enums.serializer_plugin_type import SerializerPluginType

from test_engine_app.enums.service_result import ServiceResult
from test_engine_app.enums.service_status import ServiceStatus


@dataclass
class ServiceMetadata:
    """
    ServiceMetadata class comprises information on the service such as serviceType, serviceStatus, and validationResults
    """

    status: ServiceStatus
    result: Union[ServiceResult, None]
    schema: str
    error_messages: str
    model_format: Union[ModelPluginType, None]
    data_format: Union[DataPluginType, None]
    serializer_type: Union[SerializerPluginType, None]
    data_type: str

    def __init__(self):
        self.status = ServiceStatus.INIT
        self.result = None
        self.schema = ""
        self.error_messages = ""
        self.model_format = None
        self.data_format = None
        self.serializer_type = None
        self.data_type = ""
