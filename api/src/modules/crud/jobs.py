from modules.utils.base_functions import Utilities
from modules.schemas.requests.job import GetJobRequest
from modules.schemas.responses.job import (
    JobResponse,
    create_jobresponse,
    GetJobsResponse,
    GetJobResponse,
)
from modules.schemas.queue.job_task import Job, JobState
from modules.database.models.job_task import _Job, _Task


class DbJobs(Utilities):
    async def get_job_response(self, job: Job) -> JobResponse:
        states, successes, ends = ([] for _ in range(3))
        some_tasks = False
        async with self.get_session() as session:
            result = await session.execute(
                self.select(_Task).where(_Task.job_id == job.job_id)
            )
            results = result.scalars().all()
        for res in results:
            some_tasks = True
            states.append(res.status["state"])
            successes.append(res.status["success"])
            ends.append(res.finished)

        # No tasks in DB.
        if not some_tasks:
            job.job_status["state"] = JobState.NoTasks
            job.job_status["success"] = False
            job.job_status["is_finished"] = True
            return create_jobresponse(job)

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
        elif JobState.Received in states or JobState.Pending in states:
            state = JobState.Pending
            success = False
            is_finished = False

        job.job_status["state"] = state
        job.job_status["success"] = success
        job.job_status["is_finished"] = is_finished

        return create_jobresponse(job, ends[-1])

    async def get_jobs(self, data) -> GetJobsResponse:
        jobs = list()
        async with self.get_session() as session:
            result = await session.execute(self.select(_Job))
            for job in result.scalars():
                jobs.append(await self.get_job_response(job))

        # TODO filter jobs with userid?
        return GetJobsResponse(
            jobs=jobs,
            message=f"Total number of jobs : {len(jobs)}",
        )

    async def get_job(self, data: GetJobRequest) -> GetJobResponse:
        if await self.job_exist(data.job_id) is not None:
            async with self.get_session() as session:
                query = self.select(_Job).where(_Job.job_id == data.job_id)
                jobs = await session.execute(query)
                (job,) = jobs.first()
            job_status = await self.get_job_response(job)
            return GetJobResponse(
                job=job_status,
                message=f"Success getting status for job with id: {data.job_id}.",
            )
        return GetJobResponse(
            success=False,
            message=f"Success getting status for job with id: {data.job_id}.",
        )
