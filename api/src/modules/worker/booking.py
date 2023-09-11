from modules.schemas.requests.booking import BookingModel
from modules.crud.crud_bookings import Bookings
from modules.settings.config import Settings
import asyncio


class BookingHandler:
    def __init__(self, config: Settings) -> None:
        self.cf = config

    def create_booking(self, queue_job: dict) -> tuple[bool, dict]:
        booking_request = queue_job["booking_request"]
        booking_handler = Bookings(self.cf)
        result = {}
        try:
            (response, oid) = asyncio.get_event_loop().run_until_complete(
                booking_handler._create_booking(BookingModel(**booking_request))
            )
            result["oid"] = oid
            return (response, result)
        except Exception as e:
            print("Process failed.....")
            print(e)
            return (False, {})
