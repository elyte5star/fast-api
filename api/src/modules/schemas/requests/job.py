from .base_request import RequestBase

from modules.schemas.queue.job_task import Job


class CreateJob(RequestBase):
    job: Job = None


class GetJobRequest(RequestBase):
    job_id: str = ""
