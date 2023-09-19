from modules.database.base import Base
from modules.schemas.misc.enums import JobType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    ForeignKey,
    Enum,
    JSON,PickleType
)


class _Job(Base):
    job_id = Column(String(60), primary_key=True, index=True)
    userid = Column(String(60), ForeignKey("_user.userid",onupdate="CASCADE", ondelete="CASCADE"),nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=True)
    job_type = Column(Enum(JobType))
    job_status = Column(JSON)
    number_of_tasks = Column(Integer)
    booking_request = Column(JSON(none_as_null=True))
    task_ids = Column(MutableList.as_mutable(PickleType), default=[])


class _Task(Base):
    task_id = Column(String(60), primary_key=True, index=True)
    job_id = Column(String(60), ForeignKey("_job.job_id",onupdate="CASCADE", ondelete="CASCADE"),nullable=False)
    status = Column(JSON(none_as_null=True))
    result = Column(JSON(none_as_null=True))
    created_at = Column(DateTime(timezone=True), nullable=True)
    started = Column(DateTime(timezone=True), nullable=True)
    finished = Column(DateTime(timezone=True), nullable=True)

