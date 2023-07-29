from pydantic import BaseModel
from .base_request import RequestBase
from modules.schemas.requests.product import ProductItem
from modules.schemas.requests.review import Review


class CartItem(ProductItem):
    discount: list[float]
    reviews: list[Review]
    quantity: int


class CreateBooking(BaseModel):
    cart: list[CartItem]
    total_price: str


class BookingRequest(RequestBase):
    pass


class BookingsRequest(RequestBase):
    pass
