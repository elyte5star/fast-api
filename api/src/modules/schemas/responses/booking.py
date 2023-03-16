from .base_response import BaseResponse,BaseModel
from .job import JobResponse


class CreateBookingResponse(BaseResponse):
    oid: str = ""
    volume: int = 0
    sale_price: float = 0.0



class CreateQBookingResponse(BaseModel):
    oid: str = ""
    volume: int = 0
    sale_price: float = 0.0


class GetBookingsResponse(BaseResponse):
    bookings: list = list()


class ConfirmBookingResponse(BaseResponse):
    oid: str = ""


class GetQBookingRequestResult(BaseResponse):
    job: JobResponse = JobResponse()
    result_data: CreateQBookingResponse = CreateQBookingResponse()
