from modules.schemas.worker.worker import Worker
import uuid
from datetime import datetime
from modules.settings.config import Settings
from modules.database.db_session import _Worker, _Task, _Job
from modules.schemas.misc.enums import JobType, JobStatus, JobState
import json
from pika import ConnectionParameters, BlockingConnection
from modules.schemas.misc.enums import WorkerType
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy import select, update, create_engine, URL
from pytz import timezone
from multiprocessing import Process


class BWorker(Process):
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
        Process.__init__(self)

    def time_now(self) -> datetime:
        now_utc = datetime.now()
        now_norway = now_utc.astimezone(timezone("Europe/Stockholm"))
        return now_norway

    def create_worker(self):
        worker = Worker()
        worker.worker_type = self.worker_type
        worker.created_at = self.time_now()
        worker.worker_id = self.id
        worker.queue_name = self.queue_name
        worker.queue_host = self.cf.rabbit_host_name
        return worker

    def session_generator(self):
        engine = create_engine(
            self.url_object,
            echo=False,
        )
        _, kwargs = engine.dialect.create_connect_args(engine.url)
        # print(f"[+] Connection information : {kwargs}")
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @contextmanager
    def get_session(self):
        try:
            session_local = self.session_generator()
            with session_local() as session:
                yield session
        except Exception as e:
            session.rollback()
            print(e)
            raise
        finally:
            session.close()

    def insert_worker_to_db(self, worker: Worker):
        db_worker = _Worker(**worker.dict())
        with self.get_session() as session:
            session.add(db_worker)
            session.commit()
            session.refresh(db_worker)

    def _update_ongoing_task_status_in_db(self, status_dict: dict, task_id: str):
        with self.get_session() as session:
            stmt = (
                update(_Task)
                .where(_Task.task_id == task_id)
                .values(dict(started=self.time_now(), status=status_dict))
            )
            session.execute(stmt)
            session.commit()

    def _update_finished_task_status_in_db(
        self, status_dict: dict, task_id: str, result: dict
    ):
        stmt = (
            update(_Task)
            .where(_Task.task_id == task_id)
            .values(dict(finished=self.time_now(), status=status_dict, result=result))
        )

        with self.get_session() as session:
            session.execute(stmt)
            session.commit()

    def callback(self, ch, method, properties, body):
        try:
            # Get job and task from queue item.
            # print(" [x] Received job and task %r" % json.loads(body.decode()))
            received = body.decode()
            queue_item = json.loads(received)
            queue_task = queue_item["task"]
            queue_job = queue_item["job"]
            job_type = queue_job["job_type"]

            result = {}

            # Find task in db, update started, status before doing any work.
            with self.get_session() as session:
                stmt = select(_Task).where(_Task.task_id == queue_task["task_id"])
                (db_task,) = session.execute(stmt).first()

            # Update task status
            task_status = {
                "state": JobState.Pending,
                "success": False,
                "is_finished": False,
            }
            self._update_ongoing_task_status_in_db(task_status, db_task.task_id)

            # Switch on job type.
            success = False
            match job_type:
                case JobType.Noop:
                    raise SystemExit("No job on the queue")
                case JobType.CreateSearch:
                    raise SystemExit("Create Search job in wrong queue.")
                case JobType.CreateBooking:
                    (success, result) = self.booking_handler.create_booking(queue_job)

                case _:
                    raise SystemExit(f"Unknown job type: {job_type}")
        except Exception as e:
            # On exception, put queue_item on lost_item queue.
            connection = BlockingConnection(
                ConnectionParameters(host=self.cf.rabbit_host_name)
            )
            channel = connection.channel()
            channel.queue_declare(queue=self.cf.queue_name[2], durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_publish(
                exchange="",
                routing_key=self.cf.queue_name[2],
                body=received,
            )
            channel.close()
            connection.close()
            print(f"Couldnt process task....{e}")

        finally:
            # Update task in db.
            task_status = {
                "state": JobState.Finished,
                "success": success,
                "is_finished": True,
            }
            self._update_finished_task_status_in_db(
                task_status, db_task.task_id, result
            )
            print(" [*] Result for Task. :", result)
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # rename run_forever()
    # override the run function
    def run(self) -> None:
        connection = BlockingConnection(
            ConnectionParameters(host=self.cf.rabbit_host_name)
        )
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=False)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        self.insert_worker_to_db(self.create_worker())
        print(" [*] Worker Waiting for Task.")
        channel.start_consuming()
