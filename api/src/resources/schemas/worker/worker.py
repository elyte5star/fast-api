from pydantic import BaseModel, Json
from ..misc.enums import WorkerType
from datetime import datetime


class Worker(BaseModel):
    created_at: datetime = datetime.utcnow
    worker_type: WorkerType = WorkerType.Noop
    worker_id: str = ""
    queue_name: str = ""
    queue_host: str = ""
