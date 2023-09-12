from modules.queue.base import RQHandler
from modules.schemas.misc.enums import JobType
from modules.schemas.requests.booking import BookingRequest, BookingModel
from modules.schemas.responses.job import (
    GetJobRequestResponse,
    create_jobresponse,
)
from modules.schemas.responses.booking import GetQBookingRequestResult
from modules.schemas.requests.job import GetJobRequest
from modules.database.models.job_task import _Job
from modules.schemas.queue.job_task import result_available
from sqlalchemy.orm import selectinload


class QBookingHandler(RQHandler):
    async def add_create_booking_job(
        self, data: BookingRequest
    ) -> GetJobRequestResponse:
        job = self.create_job(JobType.CreateBooking)
        total_price = data.booking.total_price
        if data.cred.discount is not None:
            total_price = self.calculate_discount(total_price, data.cred.discount)
        if await self.make_payment(data.booking.payment_details, total_price):
            booking_model = BookingModel(
                shipping_details=data.booking.billing_address
                if data.booking.shipping_details is None
                else data.booking.shipping_details,
                cart=data.booking.cart,
                userid=data.cred.userid,
                total_price=data.booking.total_price,
            )
            job.booking_request = booking_model
            job.userid = data.cred.userid
            return await self.add_job_with_one_task(job, self.cf.queue_name[1])
        return GetJobRequestResponse(success=False, message="Couldnt create job")

    async def get_booking_result(self, data: GetJobRequest) -> GetQBookingRequestResult:
        if await self.job_exist(data.job_id) is not None:
            async with self.get_session() as session:
                query = (
                    self.select(_Job)
                    .where(_Job.job_id == data.job_id)
                )
                jobs = await session.execute(query)
                (job,) = jobs.first()
                if job.job_type != JobType.CreateBooking:
                    return GetQBookingRequestResult(
                        success=False, message="Wrong job type."
                    )
                (job, tasks, end) = await self._check_job_and_tasks(job)

                # update job status in db?
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
