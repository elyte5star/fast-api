from resources.worker.base import Worker
from resources.worker.booking import BookingHandler
from resources.settings.config import Settings


def run():
    config = Settings().from_toml_file()
    worker = Worker(config)
    worker.booking_handler = BookingHandler(config)
    worker.run_forever()


if __name__ == "__main__":
    run()
