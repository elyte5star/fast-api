from resources.database.base import Base
from datetime import datetime
from ...schemas.misc.enums import JobState, JobStatus, JobType
from sqlalchemy import Column, String, DateTime,Integer, ForeignKey, Enum, JSON


class _Job(Base):
    job_id = Column(String(60), primary_key=True, index=True)
    task_id = Column(String(60), index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    username = Column(String(60), ForeignKey("user.username"))
    job_type = Column(Enum(JobType))
    job_status = Column(Enum(JobStatus))
    number_of_tasks = Column(Integer)
    booking_request = Column(JSON)


class _Task(Base):
    task_id = Column(String(60), primary_key=True, index=True)
    job_id = Column(String(60), ForeignKey("_job.job_id"))
    status = Column(Enum(JobStatus))
    result = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    started = Column(String(60), index=True)
    finished = Column(String(60), index=True)
