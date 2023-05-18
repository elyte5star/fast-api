from modules.utils.base_functions import Utilities
from modules.database.models.booking import _Booking
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from modules.schemas.requests.booking import BookingsRequest, BookingRequest
from modules.schemas.responses.booking import (
    ConfirmBookingResponse,
    CreateBookingResponse,
    GetBookingsResponse,
    BaseResponse,
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
    async def _create_booking(self, form_data: BookingRequest) -> CreateBookingResponse:
        sale_price = form_data.unit_price * form_data.volume
        if form_data.cred.discount is not None:
            sale_price = self.calculate_discount(sale_price, form_data.cred.discount)
        booking = _Booking(
            oid=self.get_indent(),
            sale_price=sale_price,
            pid=form_data.pid,
            volume=form_data.volume,
            owner_id=form_data.cred.userid,
        )

        async with self.get_session() as session:
            session.add(booking)
            await session.commit()
            return CreateBookingResponse(
                oid=booking.oid,
                volume=form_data.volume,
                sale_price=sale_price,
                message=f"Booking for {form_data.volume} item(s) created!",
            )

    async def _confirm_booking(self, oid: str) -> ConfirmBookingResponse:
        if await self.oid_exist(oid) is not None:
            query = (
                self.update(_Booking)
                .where(_Booking.oid == oid)
                .values(dict(confirmed=True))
                .execution_options(synchronize_session="fetch")
            )
            async with self.get_session() as session:
                await session.execute(query)
                await session.commit()
                return ConfirmBookingResponse(oid=oid, message="Booking confirmed!")
        return ConfirmBookingResponse(
            success=False, message="Booking not confirmed, order not found!"
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
                        bookings=bookings,
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
