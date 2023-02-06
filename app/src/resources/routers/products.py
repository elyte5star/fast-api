from fastapi import APIRouter, Depends
from resources.schemas.requests.product import (
    Product_Item,
    CreateProductsRequest,
    GetSortRequest,
    GetProductsRequest,
    GetProductDetailsRequest,
    DeleteProductRequest,
    CreateDiscountRequest,
)
from resources.schemas.responses.product import (
    GetProductsResponse,
    GetProductDetailsResponse,
    BaseResponse,
    CreateProductsResponse,
    CreateDiscountResponse,
)
from resources.schemas.requests.auth import JWTcredentials
from resources.auth.dependency import security


router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/create",
    response_model=CreateProductsResponse,
    summary="Create Products",
)
async def create_products(
    product_data_list: list[Product_Item],
    cred: JWTcredentials = Depends(security),
) -> CreateProductsResponse:
    return await handler._create_products(
        CreateProductsRequest(products=product_data_list, token_load=cred)
    )


@router.post(
    "/create_discount",
    response_model=CreateDiscountResponse,
    summary="Create discount for a product.",
)
async def create_discount(
    pid: str, discount: float, cred: JWTcredentials = Depends(security)
) -> CreateProductsResponse:
    return await handler._create_discount(
        CreateDiscountRequest(
            pid=pid,
            discount=discount,
            token_load=cred,
        )
    )


@router.get(
    "/{pid}",
    response_model=GetProductDetailsResponse,
    summary="Get one product",
)
async def get_product(pid: str) -> GetProductDetailsResponse:
    return await handler._get_product(GetProductDetailsRequest(pid=pid))


@router.delete(
    "/{pid}",
    response_model=BaseResponse,
    summary="Delete one product",
)
async def delete_product(
    pid: str, cred: JWTcredentials = Depends(security)
) -> BaseResponse:
    return await handler._delete_product(
        DeleteProductRequest(token_load=cred, pid=pid)
    )


@router.get(
    "/sort/{key}",
    response_model=GetProductsResponse,
    summary="Sort products",
)
async def sort_product(key: str) -> GetProductsResponse:
    return await handler._sort_items(GetSortRequest(key=key))


@router.get(
    "/all/products",
    response_model=GetProductsResponse,
    summary="Get all products",
)
async def get_products() -> GetProductsResponse:
    return await handler._get_products()


@router.get(
    "/deals/products",
    response_model=GetProductsResponse,
    summary="Get all deals",
)
async def special_deals() -> GetProductsResponse:
    return await handler._special_deals()
