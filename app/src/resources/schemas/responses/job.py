from datetime import datetime
from .base_response import BaseModel, BaseResponse
from ..queue.job_task import Job, JobType, JobStatus


class JobResponse(BaseModel):
    username: str = ""
    start_time: datetime = datetime(1980, 1, 1)
    end_time: datetime = datetime(1980, 1, 1)
    total_time: float = 0.0
    job_type: JobType = JobType.Noop
    job_id: str = None
    job_status: JobStatus = JobStatus()


def create_jobresponse(
    job: Job, end: datetime = datetime(1980, 1, 1)
) -> JobResponse:
    return JobResponse(
        username=job["username"],
        start_time=job["created_at"],
        job_type=job["job_type"],
        job_id=job["job_id"],
        job_status=job["job_status"],
        end_time=end,
        total_time=float((end - job["created_at"]).total_seconds()),
    )


class GetJobsResponse(BaseResponse):
    jobs: list[JobResponse] = list()


class GetJobResponse(BaseResponse):
    job: JobResponse = None


class GetJobRequestResponse(BaseResponse):
    job_id: str = ""
