from dataclasses import dataclass
from datetime import datetime

from test_engine_app.enums.task_status import TaskStatus


@dataclass
class TaskMetadata:
    """
    TaskMetadata class comprises information on the task such as name, description, and version
    """

    elapsed_time: int
    start_time: datetime
    end_time: datetime
    percentage: int
    status: TaskStatus
    results: str
    error_messages: str

    def __init__(self):
        self.elapsed_time = 0
        self.start_time = datetime.now()
        self.end_time = datetime.now()
        self.percentage = 0
        self.status = TaskStatus.PENDING
        self.results = ""
        self.error_messages = ""
