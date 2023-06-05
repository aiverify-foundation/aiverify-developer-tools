import json
from typing import Dict

from test_engine_core.utils.json_utils import remove_numpy_formats

from test_engine_app.enums.task_status import TaskStatus
from test_engine_app.processing.task_metadata import TaskMetadata


class TaskFormatter:
    """
    TaskFormatter focuses on formatting the results into the specification defined in Confluence
    """

    @staticmethod
    def format_response(metadata: TaskMetadata, log_filepath: str) -> Dict:
        """
        A method to format task update with task information.
        This method will format task information into a dictionary that is compliant with the interface specified
        in Confluence.

        Args:
            metadata (TaskMetadata): Task metadata that comprises run information
            log_filepath (str): Task log file location

        Returns:
            Dict: response dict for update.
        """
        response_dict: Dict = dict()

        if metadata.status is TaskStatus.ERROR:
            response_dict.update(
                {
                    "type": "TaskResponse",
                    "status": TaskFormatter._get_initial_case(metadata.status.name),
                    "elapsedTime": metadata.elapsed_time,
                    "startTime": metadata.start_time.isoformat(),
                    "output": metadata.results,
                    "errorMessages": str(metadata.error_messages),
                    "logFile": log_filepath,
                    "taskProgress": metadata.percentage,
                }
            )
        else:
            # Scan the dict for float32 not JSON serializable
            results = remove_numpy_formats(metadata.results)
            response_dict.update(
                {
                    "type": "TaskResponse",
                    "status": TaskFormatter._get_initial_case(metadata.status.name),
                    "elapsedTime": metadata.elapsed_time,
                    "startTime": metadata.start_time.isoformat(),
                    "output": json.dumps(results),
                    "logFile": log_filepath,
                    "taskProgress": metadata.percentage,
                }
            )
        return response_dict

    @staticmethod
    def _get_initial_case(temp_string: str) -> str:
        """
        A helper method to return init case for the temp string provided

        Args:
            temp_string (str): The string to be converted to init case

        Returns:
            str: initial-case string
        """
        lower_case_str = temp_string.lower()
        init_case_str = lower_case_str[0].upper() + lower_case_str[1:]
        return init_case_str
