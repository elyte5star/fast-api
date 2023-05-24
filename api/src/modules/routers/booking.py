from fastapi import APIRouter, Depends, Form
from modules.schemas.requests.booking import (
    CreateBooking,
    BookingsRequest,
    BookingRequest,
)
from modules.schemas.responses.booking import (
    CreateBookingResponse,
    GetBookingsResponse,
    GetBookingResponse,
)
from modules.schemas.requests.auth import JWTcredentials
from modules.auth.dependency import security

router = APIRouter(prefix="/booking", tags=["Bookings"])


# Create booking
@router.post("/create", response_model=CreateBookingResponse)
async def create_booking(
    data: CreateBooking,
    cred: JWTcredentials = Depends(security),
):
    return await handler._create_booking(
        BookingRequest(
            cart=data.cart,
            cred=cred,
        )
    )


# Get Bookings
@router.get("/all", response_model=GetBookingsResponse)
async def get_bookings(
    cred: JWTcredentials = Depends(security),
) -> GetBookingsResponse:
    return await handler._get_bookings(BookingsRequest(token_load=cred))


@router.get("/{oid}", response_model=GetBookingResponse, summary="Get one user")
async def get_booking(
    oid: str, cred: JWTcredentials = Depends(security)
) -> GetBookingResponse:
    return await handler._get_booking(
        BookingRequest(
            oid=oid,
            cred=cred,
        )
    )
