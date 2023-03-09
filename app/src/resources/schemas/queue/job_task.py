from pydantic import BaseModel, Json
from datetime import datetime
from ..misc.enums import JobState, JobStatus, JobType
from ..requests.booking import CreateBooking, BookingRequest
from typing import Optional


class Job(BaseModel):
    created_at: datetime = datetime.utcnow
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
    created_at: datetime = datetime(1985, 1, 1)
    started: datetime = datetime(1985, 1, 1)
    finished: datetime = datetime(1985, 1, 1)


def result_available(job: Job) -> bool:
    if job.job_status["is_finished"] == False:
        return False
    if job.job_status["state"] != JobState.Finished:
        return False
    return job.job_status["success"] == True
