from resources.worker.base import WorkerBase
from resources.worker.booking import BookingHandler
from resources.settings.config import Settings
from resources.schemas.misc.enums import WorkerType


def run():
    config = Settings().from_toml_file()
    worker = WorkerBase(config, WorkerType.Booking, config.queue_name[1])
    worker.booking_handler = BookingHandler(config)
    worker.run_forever()


if __name__ == "__main__":
    run()
