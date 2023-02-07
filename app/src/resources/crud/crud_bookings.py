from resources.utils.base_functions import Utilities
from resources.database.models.booking import Booking
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from resources.schemas.requests.booking import (
    CreateBooking,
    BookingsRequest,
)
from resources.schemas.responses.booking import (
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

    def calculate_discount(self, amount: float, percentage: float) -> float:
        discount = amount * percentage
        sale_price = amount - discount
        return str(round(sale_price, 2))


class Bookings(Discount):
    async def _create_booking(
        self, form_data: CreateBooking
    ) -> CreateBookingResponse:

        sale_price = form_data.unit_price * form_data.volume
        if form_data.discount is not None:
            sale_price = self.calculate_discount(
                sale_price, form_data.discount
            )
        booking = Booking(
            oid=self.get_indent(),
            sale_price=sale_price,
            pid=form_data.pid,
            volume=form_data.volume,
            owner_id=form_data.userid,
        )
        self.add(booking)
        try:
            await self.commit()
            await self.refresh(booking)
            return CreateBookingResponse(
                oid=booking.oid,
                volume=form_data.volume,
                sale_price=sale_price,
                message=f"Booking for {form_data.volume} item(s) created!",
            )
        except IntegrityError as e:
            self.log.warning(repr(e))
            await self.rollback()
            return BaseResponse(
                success=False,
                message=str(e),
            )

    async def _confirm_booking(self, oid: str) -> ConfirmBookingResponse:
        query = (
            self.update(Booking)
            .where(Booking.oid == oid)
            .values(dict(confirmed=True))
            .execution_options(synchronize_session="fetch")
        )
        await self.execute(query)
        try:
            await self.commit()
            return ConfirmBookingResponse(
                oid=oid, message="Booking confirmed!"
            )
        except IntegrityError as e:
            self.log.warning(e)
            await self.rollback()
            return ConfirmBookingResponse(
                oid=oid, success=False, message="Booking not confirmed!"
            )

    async def _get_bookings(
        self, data: BookingsRequest
    ) -> GetBookingsResponse:
        if data.token_load.username == self.cf.username:
            query = self.select(Booking).options(selectinload(Booking.owner))
            bookings = await self.execute(query)
            bookings = bookings.scalars().all()
            return GetBookingsResponse(
                bookings=bookings,
                message=f"Total number of bookings: {len(bookings)}",
            )
        return GetBookingsResponse(
            success=False,
            message="Admin rights needed!",
        )
