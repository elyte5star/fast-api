from pydantic import BaseModel, Json
from datetime import datetime
from ..misc.enums import JobState, JobStatus, JobType
from ..requests.booking import CreateBooking, BookingRequest
from typing import Optional


class Job(BaseModel):
    created_at: Optional[datetime] = None
    job_type: JobType = JobType.Noop
    job_id: str = ""
    task_id: str = ""
    job_status: JobStatus = JobStatus()
    number_of_tasks: int = 0
    booking_request: Optional[BookingRequest] = None


class Task(BaseModel):
    task_id: str = ""
    job_id: str = ""
    status: JobStatus = JobStatus()
    result: Json = None
    created_at: Optional[datetime] = None
    started: Optional[datetime] = None
    finished: Optional[datetime] = None


class Result(BaseModel):
    result_id: str = ""
    result_type: int = 0  # TODO: change to enum, 10 = database, 20 = file
    result_state: int = (
        0  #  TODO: change to enum, 10 = present, 20 = archived, 30 = removed
    )
    task_id: str = ""
    data: dict = {}  # Instead of result in Task
    data_checksum: str = None


class ResultLog(BaseModel):
    result_id: str = ""
    created_at: datetime = datetime.utcnow
    handled: bool = False
    handled_dt: datetime = None


def result_available(job: Job) -> bool:
    if job.job_status["is_finished"] == False:
        return False
    if job.job_status["state"] != JobState.Finished:
        return False
    return job.job_status["success"] == True
