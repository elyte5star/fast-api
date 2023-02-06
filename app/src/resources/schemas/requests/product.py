from .base_request import RequestBase
from pydantic import BaseModel


class GetProductDetailsRequest(BaseModel):
    pid: str


class GetProductsRequest(RequestBase):
    pass


class CreateDiscountRequest(RequestBase):
    pid = str
    discount = float


class Product_Item(BaseModel):
    name: str
    description: str
    details: str
    image: str
    price: float
    category: str


class CreateProductRequest(RequestBase):
    product: Product_Item


class CreateProductsRequest(RequestBase):
    products: list[Product_Item]


class DeleteProductRequest(RequestBase):
    pid: str


class GetSortRequest(RequestBase):
    key: str
