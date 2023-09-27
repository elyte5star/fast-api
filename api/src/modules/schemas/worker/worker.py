from pydantic import BaseModel
from ..misc.enums import WorkerType
from datetime import datetime
from typing import Optional


class Worker(BaseModel):
    created_at: datetime = datetime.utcnow
    worker_type: WorkerType = WorkerType.Noop
    worker_id: str = ""
    queue_name: str = ""
    queue_host: str = ""
    process_id: Optional[str] = ""
