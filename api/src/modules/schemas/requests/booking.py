from pydantic import BaseModel
from .base_request import RequestBase


class CreateBooking(BaseModel):
    cart: list
    total_price: str


class BookingRequest(RequestBase):
    pass


class BookingsRequest(RequestBase):
    pass
