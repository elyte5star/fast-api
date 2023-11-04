from pydantic import BaseModel, field_validator, EmailStr

from .base_request import RequestBase
from modules.schemas.requests.product import ProductItem
from modules.schemas.requests.review import Review
from typing import Optional
from modules.schemas.requests.auth import JWTcredentials


class CartItem(ProductItem):
    discount: list[float]
    reviews: list[Review]
    quantity: int
    calculated_price: float


class PaymentDetails(BaseModel):
    cardType: str
    cardNumber: str
    expiryDate: str
    cardCvv: str
    nameOnCard: str


class BillingAddress(BaseModel):
    bfname: str
    bemail: EmailStr
    baddress: str
    bcountry: str
    bzip: str
    bcity: str


class CreateBooking(BaseModel):
    cart: list[CartItem]
    total_price: float
    payment_details: PaymentDetails
    billing_address: BillingAddress
    shipping_details: Optional[BillingAddress] = None

    @field_validator("shipping_details")
    @classmethod
    def prevent_none(cls, v: BillingAddress):
        assert v is not None, "shipping_details may not be None"
        return v


class BookingModel(BaseModel):
    cart: list[CartItem]
    total_price: float
    shipping_details: BillingAddress
    userid: str


class BookingRequest(RequestBase):
    cred: JWTcredentials
    booking: Optional[CreateBooking] = None


class BookingsRequest(RequestBase):
    pass
