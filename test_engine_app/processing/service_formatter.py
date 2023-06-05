import json
from typing import Dict

from test_engine_app.enums.service_result import ServiceResult
from test_engine_app.enums.service_status import ServiceStatus
from test_engine_app.processing.service_metadata import ServiceMetadata


class ServiceFormatter:
    """
    ServiceFormatter focuses on formatting the results into the specification defined in Confluence
    """

    @staticmethod
    def format_dataset_validation_response(
        metadata: ServiceMetadata, log_filepath: str
    ) -> Dict:
        """
        A method to format service update with service information.
        This method will format service information into a dictionary that is compliant
        with the interface specified in Confluence.

        Args:
            metadata (ServiceMetadata): Service metadata that comprises run information of dataset validation
            log_filepath (str): Service log file location

        Returns:
            Dict: response dict for update.
        """
        response_dict = dict()

        if metadata.status is ServiceStatus.ERROR:
            response_dict.update(
                {
                    "type": "ServiceResponse",
                    "status": metadata.status.name.lower(),
                    "validationResult": metadata.result.name.lower(),
                    "errorMessages": metadata.error_messages,
                    "logFile": log_filepath,
                }
            )
        else:
            if metadata.result is ServiceResult.VALID:
                response_dict.update(
                    {
                        "type": "ServiceResponse",
                        "status": metadata.status.name.lower(),
                        "validationResult": metadata.result.name.lower(),
                        "serializedBy": metadata.serializer_type.name.lower(),
                        "dataFormat": metadata.data_format.name.lower(),
                        "columns": json.dumps(metadata.schema),
                        "logFile": log_filepath,
                    }
                )
            else:
                response_dict.update(
                    {
                        "type": "ServiceResponse",
                        "status": metadata.status.name.lower(),
                        "validationResult": metadata.result.name.lower(),
                        "errorMessages": metadata.error_messages,
                        "logFile": log_filepath,
                    }
                )
        return response_dict

    @staticmethod
    def format_model_validation_response(
        metadata: ServiceMetadata, log_filepath: str
    ) -> Dict:
        """
        A method to format service update with service information.
        This method will format service information into a dictionary that is compliant
        with the interface specified in Confluence.

        Args:
            metadata (ServiceMetadata): Service metadata that comprises run information of model validation
            log_filepath (str): Service log file location

        Returns:
            Dict: response dict for update.
        """
        response_dict = dict()

        if metadata.status is ServiceStatus.ERROR:
            response_dict.update(
                {
                    "type": "ServiceResponse",
                    "status": metadata.status.name.lower(),
                    "validationResult": metadata.result.name.lower(),
                    "errorMessages": metadata.error_messages,
                    "logFile": log_filepath,
                }
            )
        else:
            if metadata.result is ServiceResult.VALID:
                response_dict.update(
                    {
                        "type": "ServiceResponse",
                        "status": metadata.status.name.lower(),
                        "validationResult": metadata.result.name.lower(),
                        "serializedBy": metadata.serializer_type.name.lower(),
                        "modelFormat": metadata.model_format.name.lower(),
                        "logFile": log_filepath,
                    }
                )
            else:
                response_dict.update(
                    {
                        "type": "ServiceResponse",
                        "status": metadata.status.name.lower(),
                        "validationResult": metadata.result.name.lower(),
                        "errorMessages": metadata.error_messages,
                        "logFile": log_filepath,
                    }
                )
        return response_dict
