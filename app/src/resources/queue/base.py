from resources.utils.base_functions import Utilities
from resources.database.models.booking import Booking
from sqlalchemy.exc import IntegrityError
from aio_pika import Message, connect
from ..schemas.queue.item import ItemInQueue
from ..schemas.queue.job_task import Job, JobState, JobStatus, JobType,Task


class RQHandler(Utilities):

    def create_job(self, job_type, cred):
        job = Job()
        job.job_type = job_type
        job.username = cred.username
        job.job_id = self.get_indent()
        job.job_status.state = JobState.Pending
        job.created_at = self.time_now()
        return job

    async def add_job_tasks_to_db(self,job:Job, tasks:list[Task],queue_name: str, queue_items: list[ItemInQueue],
    ) -> (bool, str):
        try:

