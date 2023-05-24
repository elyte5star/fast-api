from pydantic import BaseModel
from .base_request import RequestBase
from modules.schemas.requests.product import ProductItem


class CreateBooking(BaseModel):
    cart: list[ProductItem]


class BookingRequest(RequestBase):
    pass


class BookingsRequest(RequestBase):
    pass

