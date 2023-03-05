from resources.utils.base_functions import Utilities
from resources.database.models.booking import Booking
from sqlalchemy.exc import IntegrityError
from aio_pika import Message, connect
from ..schemas.queue.item import ItemInQueue
from ..schemas.queue.job_task import Job, JobState, JobStatus, JobType, Task
from resources.database.models.job_task import _Job, _Task
from typing import Tuple
from ..schemas.responses.base_response import BaseResponse


class RQHandler(Utilities):
    def create_job(self, job_type, cred):
        job = Job()
        job.job_type = job_type
        job.username = cred.username
        job.job_id = self.get_indent()
        job.job_status.state = JobState.Pending
        job.created_at = self.time_now()
        return job

    async def add_job_tasks_to_db(
        self,
        job: Job,
        tasks_list: list[Task],
        queue_name: str,
        queue_items_list: list[ItemInQueue],
    ) -> Tuple[bool, str]:
        try:
            _job = _Job(**job.dict())
            self.add(_job)
            await self.commit()
            await self.refresh(_job)

            for task in tasks_list:
                aux_task = _Task(**task.dict())
                self.add(aux_task)
                await self.commit()
                await self.refresh(aux_task)

            # Perform connection
            conn = await connect(self.cf.rabbit_connect_string)

            async with conn:
                # Creating a channel
                channel = await conn.channel()
                # Declaring queue
                queue = await channel.declare_queue(queue_name)

                for queue_item in queue_items_list:
                    # Sending the message
                    await channel.default_exchange.publish(
                        Message(queue_item.json().encode()),
                        routing_key=queue.name,
                    )

            return (True, job.job_id)

        except Exception as ex:
            return (False, f"Failed to create job. {str(ex)}.")

    async def add_job_with_one_task(self, job):
        """Add a job with one task to the queue."""
        job.number_of_tasks = 1
        tasks = list()
        task = Task(job_id=job.job_id, task_id=self.get_indent())
        task.status = JobStatus(state=JobState.Received)
        task.created_at = self.time_now()
        task.finished = self.time_then()
        tasks.append(task)

        queue_items_list = []
        queue_items_list.append(ItemInQueue(job=job, task=task))

        success, message = await self.add_job_tasks_to_db(
            job,
            tasks,
            queue_items_list,
            self.cf.queue_name[1],
        )
        if success:
            return BaseResponse(message=message)

        return BaseResponse(message=message, success=False)
