from pydantic import BaseModel
from .base_request import RequestBase
from typing import Optional
from .auth import JWTcredentials


class CreateBooking(BaseModel):
    pid: str
    volume: int
    unit_price: float


class BookingRequest(CreateBooking):
    cred: Optional[JWTcredentials] = None


class BookingsRequest(RequestBase):
    pass
