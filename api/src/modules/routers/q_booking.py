from fastapi import APIRouter, Depends
from modules.schemas.requests.auth import JWTcredentials
from modules.auth.dependency import security
from modules.schemas.requests.job import GetJobRequest
from modules.schemas.requests.booking import (
    CreateBooking,
    BookingRequest,
)
from modules.schemas.responses.booking import GetQBookingRequestResult
from modules.schemas.responses.job import GetJobRequestResponse

router = APIRouter(prefix="/qbooking", tags=["QBookings"])


# Create booking
@router.post(
    "/create",
    status_code=202,
    response_model=GetJobRequestResponse,
    summary="Create a booking job",
)
async def create_booking(
    res: CreateBooking, cred: JWTcredentials = Depends(security)
) -> GetJobRequestResponse:
    return await handler.add_create_booking_job(BookingRequest(cred=cred, booking=res))


@router.get(
    "/{job_id}", response_model=GetQBookingRequestResult, summary=" Get booking result"
)
async def get_booking_result(
    job_id: str, cred: JWTcredentials = Depends(security)
) -> GetQBookingRequestResult:
    return await handler.get_booking_result(
        GetJobRequest(
            cred=cred,
            job_id=job_id,
        )
    )
