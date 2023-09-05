from modules.worker.base import WorkerBase
from modules.worker.booking import BookingHandler
from modules.settings.config import Settings
from modules.schemas.misc.enums import WorkerType


def run():
    config = Settings().from_toml_file().from_env_file()
    worker = WorkerBase(config, WorkerType.Booking, config.queue_name[1])
    worker.booking_handler = BookingHandler(config)
    worker.run_forever()


if __name__ == "__main__":
    run()
