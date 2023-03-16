from modules.schemas.responses.base_response import BaseResponse
from pydantic.types import Any
from modules.schemas.requests.product import Product_Item


class GetProductDetailsResponse(BaseResponse):
    product: Any = None


class GetProductsResponse(BaseResponse):
    products: list = list()


class CreateDiscountResponse(BaseResponse):
    sid: str = ""


class CreateProductResponse(BaseResponse):
    pid: str = ""


class CreateProductsResponse(BaseResponse):
    pids: list[str] = list()
