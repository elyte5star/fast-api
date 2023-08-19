from modules.schemas.responses.base_response import BaseResponse
from typing import Any


class GetProductDetailsResponse(BaseResponse):
    product: Any = {}


class GetProductsResponse(BaseResponse):
    products: list = list()


class CreateDiscountResponse(BaseResponse):
    sid: str = ""


class CreateProductResponse(BaseResponse):
    pid: str = ""


class CreateProductsResponse(BaseResponse):
    pids: list[str] = list()
