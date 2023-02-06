from .base_response import BaseResponse


class CreateBookingResponse(BaseResponse):
    oid: str
    volume: int
    sale_price: float


class GetBookingsResponse(BaseResponse):
    bookings: list = list()


class ConfirmBookingResponse(BaseResponse):
    oid: str = ""
