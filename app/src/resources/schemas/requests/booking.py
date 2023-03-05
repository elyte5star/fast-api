from pydantic import BaseModel
from .base_request import RequestBase
from typing import Optional
from .auth import JWTcredentials


class CreateBooking(RequestBase):
    pid: str
    volume: int
    unit_price: float
    # token_load: Optional[JWTcredentials] = None


class BookingRequest(RequestBase):
    booking_request: CreateBooking = None


class BookingsRequest(RequestBase):
    pass
