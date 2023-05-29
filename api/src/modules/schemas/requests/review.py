from .base_request import RequestBase
from pydantic import BaseModel, EmailStr


class Review(BaseModel):
    reviewer_name: str
    email: EmailStr
    rating: int
    product_id: str
    comment: str


class ReviewRequest(RequestBase):
    review: Review
