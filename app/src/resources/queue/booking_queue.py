from .base import RQHandler
from resources.schemas.requests.booking import BookingRequest
from resources.schemas.responses.job import GetJobRequestResponse
from .base import JobType
from fastapi.encoders import jsonable_encoder


class QBookingHandler(RQHandler):
    async def add_create_booking_job(
        self, booking_data: BookingRequest
    ) -> GetJobRequestResponse:
        job = self.create_job(JobType.CreateBooking, booking_data.cred)
        json_obj = jsonable_encoder(booking_data.booking_request)
        job.booking_request = json_obj
        return await self.add_job_with_one_task(job)
