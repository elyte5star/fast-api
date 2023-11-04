from modules.worker.worker import BWorker
from modules.worker.booking import BookingHandler
from modules.settings.config import Settings
from modules.schemas.misc.enums import WorkerType
import time
from datetime import datetime


def main():
    config = Settings().from_toml_file().from_env_file()
    start = time.time()
    worker = BWorker(config, WorkerType.Booking, config.queue_name[1])
    worker.booking_handler = BookingHandler(config)
    worker.start()
    end = time.time()
    print(
        f"Started process with process id: {worker.pid} for worker with id: {worker.id} in {end - start} seconds. {worker.time_now()}"
    )
    worker.join()
    # worker.run_forever()


if __name__ == "__main__":
    main()
