from pydantic import BaseModel, field_validator
from .base_request import RequestBase
from modules.schemas.requests.product import ProductItem
from modules.schemas.requests.review import Review
from typing import Optional


class CartItem(ProductItem):
    discount: list[float]
    reviews: list[Review]
    quantity: int
    calculated_price: float


class CreateBooking(BaseModel):
    cart: list[CartItem]
    total_price: float
    payment_details: dict
    billing_address: dict
    shipping_details: Optional[dict] = None

    @field_validator("shipping_details")
    @classmethod
    def prevent_none(cls, v: dict):
        assert v is not None, "shipping_details may not be None"
        return v


class BookingRequest(RequestBase):
    pass


class BookingsRequest(RequestBase):
    pass
