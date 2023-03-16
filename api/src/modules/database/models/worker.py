from modules.database.base import Base
from ...schemas.misc.enums import WorkerType

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum,
)


class _Worker(Base):
    created_at = Column(DateTime(timezone=True))
    worker_type = Column(Enum(WorkerType))
    worker_id= Column(String(60), primary_key=True, index=True)
    queue_name= Column(String(60))
    queue_host= Column(String(60))
