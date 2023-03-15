from .crud_bookings import Discount
from resources.schemas.requests.product import (
    CreateProductRequest,
    CreateProductsRequest,
    GetProductDetailsRequest,
    GetProductsRequest,
    GetSortRequest,
    DeleteProductRequest,
    Product_Item,
    CreateDiscountRequest,
)
from resources.schemas.responses.product import (
    CreateProductResponse,
    CreateProductsResponse,
    GetProductDetailsResponse,
    GetProductsResponse,
    BaseResponse,
    CreateDiscountResponse,
)
from sqlalchemy.exc import IntegrityError
from resources.database.models.product import Product, SpecialDeals
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import selectinload


class Products(Discount):
    async def _create_product(
        self, data: Product_Item
    ) -> CreateProductResponse:
        product = Product(**data.dict(), pid=self.get_indent())
        self.add(product)
        try:
            await self.commit()
            return CreateProductResponse(
                pid=product.pid,
                message=f"Product with name {product.name} created!",
            )
        except IntegrityError as e:
            self.log.info(e)
            await self.rollback()
            return BaseResponse(
                success=False,
                message=str(e),
            )
        finally:
            await self._engine.dispose()

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
            message="Admin rights needed!",
        )

    async def _get_product(
        self, prod_data: GetProductDetailsRequest
    ) -> GetProductDetailsResponse:
        query = (
            self.select(Product)
            .where(Product.pid == prod_data.pid)
            .options(selectinload(Product.discount))
        )
        products = await self.execute(query)
        (product,) = products.first()
        return GetProductDetailsResponse(
            product=product, message=f"Product with id:{product.pid} found!"
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
            self.add(aux_prod)
            try:
                await self.commit()
                return CreateDiscountResponse(
                    sid=aux_prod.sid,
                    message=f"Discount created for Product with id {aux_prod.product_id}!",
                )
            except IntegrityError as e:
                self.log.warning(e)
                await self.rollback()
                return BaseResponse(
                    success=False,
                    message=str(e),
                )
            finally:
                await self._engine.dispose()

        return BaseResponse(
            success=False,
            message="Admin rights needed!",
        )

    async def _get_products(self) -> GetProductsResponse:
        query = self.select(Product).options(selectinload(Product.discount))
        products = await self.execute(query)
        products = products.scalars().all()
        return GetProductsResponse(
            products=products,
            message=f"Total number of products: {len(products)}",
        )

    async def _delete_product(
        self, data: DeleteProductRequest
    ) -> BaseResponse:
        if data.token_load.username == self.cf.username:
            query = self.delete(Product).where(Product.pid == data.pid)
            await self.execute(query)
            try:
                await self.commit()
                return BaseResponse(
                    message=f"User with id:{data.pid} deleted",
                )
            except IntegrityError as e:
                self.log.warning(repr(e))
                await self.rollback()
                return BaseResponse(
                    success=False,
                    message=str(e),
                )
            finally:
                await self._engine.dispose()
        return BaseResponse(
            success=False,
            message="Admin rights needed!",
        )

    async def _special_deals(self) -> list:
        query = self.select(SpecialDeals)
        products = await self.execute(query)
        products = products.scalars().all()
        return GetProductsResponse(
            products=products,
            message=f"Total number of special deals : {len(products)}",
        )

    async def _sort_items(self, data: GetSortRequest) -> GetProductsResponse:
        model_res = await self._get_products()
        res_orm_list = model_res.products
        res_list = jsonable_encoder(res_orm_list)
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
