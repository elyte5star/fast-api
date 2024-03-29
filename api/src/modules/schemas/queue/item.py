from pydantic import BaseModel
from typing import Optional
from .job_task import Job, Task


class QueueItem(BaseModel):
    job: Optional[Job] = None
    task: Optional[Task] = None
