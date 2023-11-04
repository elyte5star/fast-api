from multiprocessing import Process
from modules.settings.config import Settings
from modules.schemas.misc.enums import WorkerType
import uuid
from sqlalchemy import URL
from pytz import timezone
from datetime import datetime


class WorkerBase(Process):
    def __init__(
        self, config: Settings, worker_type: WorkerType, queue_name: str
    ) -> None:
        self.cf = config
        self.id = str(uuid.uuid4())
        self.worker_type = worker_type
        self.queue_name = queue_name
        self.url_object = URL.create(
            "mariadb+mariadbconnector",
            username=self.cf.sql_username,
            password=self.cf.sql_password,
            host=self.cf.sql_host,
            database=self.cf.sql_db,
        )

    def time_now(self) -> datetime:
        now_utc = datetime.now()
        now_norway = now_utc.astimezone(timezone("Europe/Stockholm"))
        return now_norway
