from .base_request import RequestBase
from pydantic import BaseModel
from typing import Any


class GetProductDetailsRequest(BaseModel):
    pid: str


class GetProductsRequest(RequestBase):
    pass


class CreateDiscountRequest(RequestBase):
    pid: str
    discount: float


class ProductItem(BaseModel):
    pid: str = ""
    name: str
    description: str
    details: str
    image: str
    price: float
    category: str
    stock_quantity: int


class CreateProductRequest(RequestBase):
    product: ProductItem


class CreateProductsRequest(RequestBase):
    products: list[ProductItem]


class DeleteProductRequest(RequestBase):
    pid: str


class GetSortRequest(RequestBase):
    key: str
