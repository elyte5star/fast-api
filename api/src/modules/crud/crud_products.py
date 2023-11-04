from .crud_bookings import Discount
from modules.schemas.requests.product import (
    CreateProductRequest,
    CreateProductsRequest,
    GetProductDetailsRequest,
    GetSortRequest,
    DeleteProductRequest,
    ProductItem,
    CreateDiscountRequest,
)
from modules.schemas.responses.product import (
    CreateProductResponse,
    CreateProductsResponse,
    GetProductDetailsResponse,
    GetProductsResponse,
    BaseResponse,
    CreateDiscountResponse,
)
from modules.schemas.responses.review import CreateReviewResponse
from modules.database.models.product import Product, SpecialDeals
from modules.database.models.review import Review
from modules.schemas.requests.review import ReviewRequest
from sqlalchemy.orm import selectinload

admin_msg = "Admin rights needed!"


class Products(Discount):
    async def _create_product(self, data: ProductItem) -> CreateProductResponse:
        if await self.product_name_exist(data.name) is None:
            data.pid = self._get_indent()
            product = Product(created_at=self.time_now(), **data.dict())
            async with self.get_session() as session:
                session.add(product)
                await session.commit()
                return CreateProductResponse(
                    pid=product.pid,
                    message=f"Product with name {product.name} created!",
                )

        return BaseResponse(
            success=False,
            message=f"Product with name {data.name} already exists!!",
        )

    async def _create_review(self, data: ReviewRequest) -> CreateReviewResponse:
        if await self.pid_exist(data.review.product_id) is not None:
            data.review.rid = self._get_indent()
            review = Review(created_at=self.time_now(),**data.review.dict())
            async with self.get_session() as session:
                session.add(review)
                await session.commit()
                return CreateReviewResponse(
                    rid=review.rid,
                    message=f"Review with id {review.rid} created!",
                )
        return CreateReviewResponse(
            success=False,
            message="Cant create review! Product doesnt exist!",
        )

    async def _create_products(
        self, data: CreateProductsRequest
    ) -> CreateProductsResponse:
        # check if admin
        if data.token_load.username == self.cf.username:
            product_ids = []
            for product_data in data.products:
                model = await self._create_product(product_data)
                product_ids.append(model.pid)
            return CreateProductsResponse(
                pids=product_ids,
                message=f"{len(product_ids)} products created!",
            )
        return CreateProductsResponse(
            success=False,
            message=admin_msg,
        )

    async def _get_product(
        self, prod_data: GetProductDetailsRequest
    ) -> GetProductDetailsResponse:
        if await self.pid_exist(prod_data.pid) is not None:
            async with self.get_session() as session:
                query = (
                    self.select(Product)
                    .where(Product.pid == prod_data.pid)
                    .options(selectinload(Product.discount))
                    .options(selectinload(Product.reviews))
                )
                result = await session.execute(query)

                (product,) = result.first()
                return GetProductDetailsResponse(
                    product=self.obj_as_json(product),
                    message=f"Product with id:{product.pid} found!",
                )
        return GetProductDetailsResponse(
            success=False, message=f"Product with id:{prod_data.pid} not found!"
        )

    async def _create_discount(self, data: CreateDiscountRequest):
        if data.token_load.username == self.cf.username:
            product_response = await self._get_product(
                GetProductDetailsRequest(pid=data.pid)
            )
            product = product_response.product
            new_price = self.calculate_discount(product.price, data.discount)
            aux_prod = SpecialDeals(
                sid=self.get_indent(),
                new_price=new_price,
                product_id=data.pid,
                discount=data.discount,
            )
            async with self.get_session() as session:
                session.add(aux_prod)
                await session.commit()
                return CreateDiscountResponse(
                    sid=aux_prod.sid,
                    message=f"Discount created for Product with id {aux_prod.product_id}!",
                )

        return BaseResponse(
            success=False,
            message=admin_msg,
        )

    async def _get_products(self) -> GetProductsResponse:
        async with self.get_session() as session:
            result = await session.execute(
                self.select(Product)
                .options(selectinload(Product.discount))
                .options(selectinload(Product.reviews))
            )
            products = result.scalars().all()

        return GetProductsResponse(
            products=self.obj_as_json(products),
            message=f"Total number of products: {len(products)}",
        )

    async def _delete_product(self, data: DeleteProductRequest) -> BaseResponse:
        if data.token_load.username == self.cf.username:
            if await self.pid_exist(data.pid) is not None:
                async with self.get_session() as session:
                    await session.execute(
                        self.delete(Product).where(Product.pid == data.pid)
                    )
                    await session.commit()
                    return BaseResponse(
                        message=f"User with id:{data.pid} deleted",
                    )

            return BaseResponse(
                success=False,
                message=f"Product with id:{data.pid} doesnt exist!",
            )
        return BaseResponse(
            success=False,
            message=admin_msg,
        )

    async def _special_deals(self) -> list:
        async with self.get_session() as session:
            result = await session.execute(self.select(SpecialDeals))
            deals = result.scalars().all()
            if len(deals) > 0:
                return GetProductsResponse(
                    products=self.obj_as_json(deals),
                    message=f"Total number of special deals : {len(deals)}",
                )
            return GetProductsResponse(
                success=False,
                message="No special deals",
            )

    async def _sort_items(self, data: GetSortRequest) -> GetProductsResponse:
        model_res = await self._get_products()
        res_orm_list = model_res.products
        res_list = self.obj_as_json(res_orm_list)
        response_list, message = (None for x in range(2))
        if data.key == "deals":
            response_list = [x for x in res_list if x["discount"]]
            message = data.key
        elif data.key == "numeric_asc":
            message = "Product prices in ascending order."
            response_list = sorted(
                res_list,
                key=lambda x: x["price"],
                reverse=False,
            )
        elif data.key == "numeric_desc":
            message = "Product prices in descending order."
            response_list = sorted(
                res_list,
                key=lambda x: x["price"],
                reverse=True,
            )
        elif data.key == "name_asc":
            message = "Product names in ascending order."
            response_list = sorted(
                res_list,
                key=lambda x: x["name"],
                reverse=False,
            )

        elif data.key == "name_desc":
            message = "Product names in descending order"
            response_list = sorted(
                res_list,
                key=lambda x: x["name"],
                reverse=True,
            )
        else:
            return BaseResponse(
                success=False,
                message=f"Unkown search key :{data.key}",
            )
        return GetProductsResponse(products=response_list, message=message)
