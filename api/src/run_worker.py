from modules.worker.worker import BWorker
from modules.worker.booking import BookingHandler
from modules.settings.config import Settings
from modules.schemas.misc.enums import WorkerType


def run():
    config = Settings().from_toml_file().from_env_file()
    worker = BWorker(config, WorkerType.Booking, config.queue_name[1])
    worker.booking_handler = BookingHandler(config)
    worker.start()
    # wait for the process to finish
    print("Waiting for the process to finish")
    worker.join()
    # worker.run_forever()


if __name__ == "__main__":
    run()
