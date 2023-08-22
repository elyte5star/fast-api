from modules.utils.base_functions import Utilities
from modules.database.models.booking import _Booking
from sqlalchemy.orm import selectinload
from modules.schemas.requests.booking import BookingsRequest, BookingRequest
from modules.schemas.responses.booking import (
    GetBookingResponse,
    CreateBookingResponse,
    GetBookingsResponse,
)

# ======================================#
# Discount by volume and by sales-amount#
# ======================================#


class Discount(Utilities):
    def low_discount_volume(self, volume: str, sale_amount: float) -> float:
        if volume <= 1500:
            return self.calculate_discount(sale_amount, 0.1)  # 10% discount
        return sale_amount

    def high_discount_volume(self, volume: str, sale_amount: float) -> float:
        volume = int(volume)
        if volume <= 10000:
            return self.calculate_discount(sale_amount, 0.3)  # 30% discount
        return sale_amount

    def low_discount_sale_amount(self, sale_amount: float) -> float:
        if sale_amount <= 1000:
            return self.calculate_discount(sale_amount, 0.1)  # 10% discount
        return sale_amount

    def high_discount_sale_amount(self, sale_amount: float) -> float:
        if sale_amount <= 100000:
            return self.calculate_discount(sale_amount, 0.3)  # 30% discount
        return sale_amount

    def calculate_discount(self, amount: float, percentage: float) -> str:
        discount = amount * percentage
        sale_price = amount - discount
        return str(round(sale_price, 2))


class Bookings(Discount):
    async def _create_booking(self, data: BookingRequest) -> CreateBookingResponse:
        total_price = float(data.total_price)
        if data.cred.discount is not None:
            total_price = self.calculate_discount(total_price, data.cred.discount)
        async with self.get_session() as session:
            booking = _Booking(
                oid=self._get_indent(),
                total_price=total_price,
                cart=data.cart,
                owner_id=data.cred.userid,
            )
            session.add(booking)
            await session.commit()
        return CreateBookingResponse(
            oid=booking.oid,
            message=f"Booking with id : {booking.oid} created!",
        )

    async def _get_bookings(self, data: BookingsRequest) -> GetBookingsResponse:
        if data.token_load.username == self.cf.username:
            async with self.get_session() as session:
                result = await session.execute(
                    self.select(_Booking).options(selectinload(_Booking.owner))
                )
                bookings = result.scalars().all()
                if bookings:
                    return GetBookingsResponse(
                        bookings=self.obj_as_json(bookings),
                        message=f"Total number of bookings: {len(bookings)}",
                    )
                return GetBookingsResponse(
                    success=False,
                    message="No Bookings found.!",
                )
        return GetBookingsResponse(
            success=False,
            message="Admin rights needed!",
        )

    async def _get_booking(self, data: BookingRequest) -> GetBookingResponse:
        if await self.oid_exist(data.oid) is not None:
            async with self.get_session() as session:
                result = await session.execute(
                    self.select(_Booking)
                    .where(_Booking.oid == data.oid)
                    .options(selectinload(_Booking.owner))
                )

                (booking,) = result.first()
                return GetBookingResponse(
                    booking=self.obj_as_json(booking),
                    message=f"Booking with id :{data.oid} found!",
                )
        return GetBookingResponse(
            success=False,
            message=f"Booking with id:{data.oid} not found!!",
        )
