from fastapi import APIRouter, Depends
from resources.schemas.requests.auth import JWTcredentials
from resources.auth.dependency import security
from resources.schemas.requests.job import GetJobRequest
from resources.schemas.requests.booking import (
    CreateBooking,
    BookingRequest,
)
from resources.schemas.responses.booking import GetQBookingRequestResult
from resources.schemas.responses.job import GetJobRequestResponse

router = APIRouter(prefix="/q_booking", tags=["QBookings"])


# Create booking
@router.post("/create", status_code=202, response_model=GetJobRequestResponse)
async def create_booking(
    booking: CreateBooking, cred: JWTcredentials = Depends(security)
) -> GetJobRequestResponse:
    return await handler.add_create_booking_job(
        BookingRequest(cred=cred, **booking.dict())
    )


@router.get("/{job_id}", response_model=GetQBookingRequestResult)
async def get_booking_result(
    job_id: str, cred: JWTcredentials = Depends(security)
) -> GetQBookingRequestResult:
    return await handler.get_booking_result(
        GetJobRequest(
            cred=cred,
            job_id=job_id,
        )
    )
