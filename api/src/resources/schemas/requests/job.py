from .base_request import RequestBase

from ..queue.job_task import Job


class CreateJob(RequestBase):
    job: Job = None


class GetJobRequest(RequestBase):
    job_id: str = ""
