from resources.utils.base_functions import Utilities
from resources.database.models.booking import Booking
from sqlalchemy.exc import IntegrityError
from aio_pika import Message, connect
from ..schemas.queue.item import ItemInQueue
from ..schemas.queue.job_task import Job, JobState, JobStatus, JobType, Task
from resources.database.models.job_task import _Job, _Task
from resources.schemas.responses.job import GetJobRequestResponse


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
    ) -> tuple[bool, str]:
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
                _ = await channel.declare_queue(queue_name)

                for queue_item in queue_items_list:
                    # Sending the message
                    await channel.default_exchange.publish(
                        Message(queue_item.json().encode()),
                        routing_key=queue_name,
                    )

            return (True, f"Job with id '{job.job_id}' created.")

        except Exception as ex:
            await self.rollback()
            return (False, f"Failed to create job. {str(ex)}.")

    async def add_job_with_one_task(self, job):
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
            self.cf.queue_name[1],
            queue_items_list,
        )
        if success:
            return GetJobRequestResponse(job_id=job.job_id, message=message)
        return GetJobRequestResponse(message=message, success=False)

    async def _check_job_and_tasks(self, job: Job) -> tuple[Job, list[Task]]:
        states = []
        successes = []
        ends = []
        tasks = []
        query = self.select(_Task).where(_Task.job_id == job.job_id)
        results = await self.execute(query)
        async for result in results:
            states.append(result["status"]["state"])
            successes.append(result["status"]["success"])
            ends.append(result["finished"])
            tasks.append(result)

        # No tasks in database.
        if len(tasks) == 0:
            job["job_status"]["state"] = JobState.NoTasks
            job["job_status"]["success"] = False
            job["job_status"]["is_finished"] = True
            return (job, [])

        ends.sort()

        success = True
        state = JobState.Finished
        is_finished = True

        if JobState.Timeout in states:
            state = JobState.Timeout
            success = False
            is_finished = True
        elif JobState.NotSet in states:
            state = JobState.NotSet
            success = False
            is_finished = False
        elif JobState.Received in states:
            state = JobState.Pending
            success = False
            is_finished = False
        elif JobState.Pending in states:
            state = JobState.Pending
            success = False
            is_finished = False

        job["job_status"]["state"] = state
        job["job_status"]["success"] = success
        job["job_status"]["is_finished"] = is_finished

        return (job, tasks, ends[-1])
