from fastapi import APIRouter, Depends, Form
from resources.schemas.requests.booking import (
    CreateBooking,
    BookingsRequest,
    BookingRequest,
)
from resources.schemas.responses.booking import (
    ConfirmBookingResponse,
    CreateBookingResponse,
    GetBookingsResponse,
)
from resources.schemas.requests.auth import JWTcredentials
from resources.auth.dependency import security

router = APIRouter(prefix="/booking", tags=["Bookings"])


# Create booking
@router.post("/create", response_model=CreateBookingResponse)
async def create_booking(
    pid: str = Form(default=None),
    volume: int = Form(default=None),
    unit_price: float = Form(default=None),
    cred: JWTcredentials = Depends(security),
):
    return await handler._create_booking(
        BookingRequest(
            pid=pid,
            volume=volume,
            unit_price=unit_price,
            cred=cred,
        )
    )


# Confirm booking
@router.get("/confirm/{oid}", response_model=ConfirmBookingResponse)
async def confirm_booking(
    oid: str, cred: JWTcredentials = Depends(security)
) -> ConfirmBookingResponse:
    return await handler._confirm_booking(oid=oid)


# Get Bookings
@router.get("/all", response_model=GetBookingsResponse)
async def get_bookings(
    cred: JWTcredentials = Depends(security),
) -> GetBookingsResponse:
    return await handler._get_bookings(BookingsRequest(token_load=cred))
