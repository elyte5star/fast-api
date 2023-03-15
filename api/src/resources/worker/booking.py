from ..schemas.queue.job_task import Job
from ..schemas.requests.booking import BookingRequest
from ..crud.crud_bookings import Bookings
from ..settings.config import Settings
import asyncio


class BookingHandler:
    def __init__(self, config: Settings) -> None:
        self.cf = config

    def create_booking(self, job: Job) -> tuple[bool, dict]:
        booking_request = job["booking_request"]
        bookings = Bookings(self.cf)
        result = None
        try:
            result = asyncio.get_event_loop().run_until_complete(
                bookings._create_booking(BookingRequest(**booking_request))
            )
            return (True, result.dict(exclude={"success", "message"}))
        except Exception as e:
            print("Process failed.....")
            print(e)
            return (False, {})
