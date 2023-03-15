from .base import RQHandler
from resources.schemas.requests.booking import BookingRequest
from resources.schemas.responses.job import (
    GetJobRequestResponse,
    create_jobresponse,
)
from resources.schemas.responses.booking import GetQBookingRequestResult
from .base import JobType
from fastapi.encoders import jsonable_encoder
from resources.schemas.requests.job import GetJobRequest
from resources.database.models.job_task import _Job
from ..schemas.queue.job_task import result_available


class QBookingHandler(RQHandler):
    async def add_create_booking_job(
        self, booking_data: BookingRequest
    ) -> GetJobRequestResponse:
        job = self.create_job(JobType.CreateBooking)
        json_obj = jsonable_encoder(booking_data)
        job.booking_request = json_obj
        return await self.add_job_with_one_task(job, self.cf.queue_name[1])

    async def get_booking_result(
        self, data: GetJobRequest
    ) -> GetQBookingRequestResult:
        query = self.select(_Job).where(_Job.job_id == data.job_id)
        jobs = await self.execute(query)
        (job,) = jobs.first()
        
        if job is not None:
            if job.job_type != JobType.CreateBooking:
                return GetQBookingRequestResult(
                    success=False, message="Wrong job type."
                )
            (job, tasks, end) = await self._check_job_and_tasks(job)

            if not result_available(job):
                return GetQBookingRequestResult(
                    success=False, message="Result from job is not available."
                )
            return GetQBookingRequestResult(
                job=create_jobresponse(job, end),
                result_data=tasks[0].result,
                message=f"Success result for job with id: {data.job_id}.",
            )

        return GetQBookingRequestResult(
            success=False, message=f"Job with id: {data.job_id} not found."
        )
