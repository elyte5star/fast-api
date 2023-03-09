from ..schemas.worker.worker import Worker
import uuid
from datetime import datetime
from ..settings.config import Settings
from ..database.db_session import AsyncDatabaseSession, _Worker, _Task, _Job
from ..schemas.misc.enums import JobType, JobStatus, JobState
from sqlalchemy.exc import IntegrityError
import json
import asyncio
from pika import ConnectionParameters, BlockingConnection
from ..schemas.misc.enums import WorkerType


class WorkerBase:
    def __init__(
        self, config: Settings, worker_type: WorkerType, queue_name: str
    ) -> None:
        self.cf = config
        self.db = AsyncDatabaseSession(self.cf)
        self.id = str(uuid.uuid4())
        self.worker_type = worker_type
        self.queue_name = queue_name

    def create_worker(self):
        worker = Worker()
        worker.worker_type = self.worker_type
        worker.created_at = datetime.utcnow()
        worker.worker_id = self.id
        worker.queue_name = self.queue_name
        worker.queue_host = self.cf.rabbit_host_name
        return worker

    def insert_worker_to_db(self, worker: Worker):
        db_worker = _Worker(**worker.dict())
        self.db.add(db_worker)
        try:
            asyncio.get_event_loop().run_until_complete(self.db.commit())
        except IntegrityError as e:
            asyncio.get_event_loop().run_until_complete(self.db.rollback())
            raise SystemExit(e)

    def _update_ongoing_task_status_in_db(
        self, status_dict: dict, task_id: str
    ):
        query = (
            self.db.update(_Task)
            .where(_Task.task_id == task_id)
            .values(
                dict(
                    started=datetime.utcnow(),
                    status=status_dict,
                )
            )
            .execution_options(synchronize_session="fetch")
        )
        query_execute = self.db.execute(query)
        commit_changes = self.db.commit()
        try:
            asyncio.get_event_loop().run_until_complete(query_execute)
            asyncio.get_event_loop().run_until_complete(commit_changes)
        except Exception as e:
            print(f"Couldnt update Task Status to pending..{e}")

    def _update_finished_task_status_in_db(
        self, status_dict: dict, task_id: str, result: dict
    ):
        query = (
            self.db.update(_Task)
            .where(_Task.task_id == task_id)
            .values(
                dict(
                    finished=datetime.utcnow(),
                    status=status_dict,
                    result=result,
                )
            )
            .execution_options(synchronize_session="fetch")
        )
        query_execute = self.db.execute(query)
        commit_changes = self.db.commit()
        try:
            asyncio.get_event_loop().run_until_complete(query_execute)
            asyncio.get_event_loop().run_until_complete(commit_changes)
        except Exception as e:
            print(f"Couldnt update Task Status to finished..{e}")

    def callback(self, ch, method, properties, body):
        try:
            # Get job and task from queue item.
            print(" [x] Received %r" % json.loads(body.decode()))
            received = body.decode()
            queue_item = json.loads(received)
            queue_task = queue_item["task"]
            queue_job = queue_item["job"]
            job_type = queue_job["job_type"]

            result = {}

            # Find task in db, update started, status before doing any work.
            query = self.db.select(_Task).where(
                _Task.task_id == queue_task["task_id"]
            )

            db_tasks = asyncio.get_event_loop().run_until_complete(
                self.db.execute(query)
            )
            (db_task,) = db_tasks.first()
            # Update task status
            task_status = {
                "state": JobState.Pending,
                "success": False,
                "is_finished": False,
            }
            self._update_ongoing_task_status_in_db(
                task_status, db_task.task_id
            )

            # Switch on job type.
            success = False
            match job_type:
                case JobType.Noop:
                    raise Exception("No job on the queue")
                case JobType.CreateSearch:
                    raise Exception("Create Search job in wrong queue.")
                case JobType.CreateBooking:
                    (success, result) = self.booking_handler.create_booking(
                        queue_job
                    )

                case _:
                    raise Exception(f"Unknown job type: {job_type}")
        except Exception as e:
            # On exception, put queue_item on lost_item queue.
            connection = BlockingConnection(
                ConnectionParameters(host=self.rabbit_host_name)
            )
            channel = connection.channel()
            channel.queue_declare(
                queue=self.cf.queue_name[2], durable=True
            )  # durable?
            channel.basic_qos(prefetch_count=1)
            channel.basic_publish(
                exchange="",
                routing_key=self.cf.queue_name[2],
                body=received,
            )
            # channel.close()
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
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def run_forever(self) -> None:
        connection = BlockingConnection(
            ConnectionParameters(host=self.cf.rabbit_host_name)
        )
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=False)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback
        )
        self.insert_worker_to_db(self.create_worker())
        print(" [*] Waiting for Task.")
        channel.start_consuming()
