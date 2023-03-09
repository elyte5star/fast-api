from ..schemas.queue.job_task import Job
from ..schemas.requests.booking import CreateBooking, BookingRequest
from ..crud.crud_bookings import Bookings
from ..settings.config import Settings
import asyncio


class BookingHandler:
    def __init__(self, config: Settings) -> None:
        self.cf = config

    def create_booking(self, job: Job):
        booking_request = job["booking_request"]
        bookings = Bookings(self.cf)
        result = None
        try:
            result = asyncio.get_event_loop().run_until_complete(
                bookings._create_booking(BookingRequest(**booking_request))
            )
            print(result)
            return (True, dict(result))
        except Exception as e:
            print("Process failed.....")
            print(e)
            return (False, {})
