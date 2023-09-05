from datetime import datetime
from .base_response import BaseModel, BaseResponse
from ..queue.job_task import Job, JobType, JobStatus
from typing import Optional


class JobResponse(BaseModel):
    userid: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_time: float = 0.0
    job_type: JobType = JobType.Noop
    job_id: str = ""
    job_status: JobStatus = JobStatus()


def create_jobresponse(job: Job, end: Optional[datetime] = None) -> JobResponse:
    return JobResponse(
        userid=job.userid,
        start_time=job.created_at,
        job_type=job.job_type,
        job_id=job.job_id,
        job_status=job.job_status,
        end_time=end,
        total_time=float((end - job.created_at).total_seconds()),
    )


class GetJobsResponse(BaseResponse):
    jobs: list[JobResponse] = list()


class GetJobResponse(BaseResponse):
    job: Optional[JobResponse] = None


class GetJobRequestResponse(BaseResponse):
    job_id: str = ""
