from .base_response import BaseResponse,BaseModel
from .job import JobResponse
from typing import Any

class CreateBookingResponse(BaseResponse):
    oid: str = ""
    

class CreateQBookingResponse(BaseModel):
    oid: str = ""
   


class GetBookingsResponse(BaseResponse):
    bookings: list = list()


class GetBookingResponse(BaseResponse):
   booking: Any = {}


class GetQBookingRequestResult(BaseResponse):
    job: JobResponse = JobResponse()
    result_data: CreateQBookingResponse = CreateQBookingResponse()
