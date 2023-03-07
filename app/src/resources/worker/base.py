from ..schemas.worker.worker import Worker
import uuid
from datetime import datetime
from ..settings.config import Settings
from ..database.db_session import AsyncDatabaseSession, _Worker, _Task, _Job
from ..schemas.misc.enums import JobType, JobStatus, JobState
from sqlalchemy.exc import IntegrityError
import json
import asyncio
import pika


class WorkerHandler:
    def __init__(self, config: Settings) -> None:
        self.cf = config
        self.db = AsyncDatabaseSession(self.cf)
        self.id = str(uuid.uuid4())

    def create_worker(self, worker_type, queue_name):
        worker = Worker()
        worker.worker_type = worker_type
        worker.created_at = datetime.utcnow()
        worker.worker_id = self.id
        worker.queue_name = queue_name
        worker.queue_host = self.cf.rabbit_host_name
        return worker

    def insert_worker_to_db(self, worker: Worker):
        db_worker = _Worker(**worker.dict())
        self.add(db_worker)
        try:
            asyncio.get_event_loop().run_until_complete(self.db.commit())
        except IntegrityError as e:
            asyncio.get_event_loop().run_until_complete(self.db.rollback())
            raise SystemExit(e)

    def close(self):
        self.channel.close()
        self.connection.close()

    def callback(self, ch, method, properties, body):
        try:
            # Get job and task from queue item.
            received = body.decode()
            queue_item = json.loads(received)
            queue_task = queue_item["task"]
            queue_job = queue_item["job"]
            job_type = queue_job["job_type"]
            result = {}

            # Find task in db, update started, status before doing any work.
            query = self.select(_Task).where(
                _Task.task_id == queue_task["task_id"]
            )

            db_task = asyncio.get_event_loop().run_until_complete(
                self.execute(query)
            )
            # Update task status
            task_status = {
                "state": JobState.Pending,
                "success": False,
                "is_finished": False,
            }
            print(task_status)
            query = (
                self.db.update(_Task)
                .where(_Task.task_id == db_task["task_id"])
                .values(
                    dict(
                        started=datetime.utcnow(),
                        status=json.dumps(task_status),
                    )
                )
                .execution_options(synchronize_session="fetch")
            )
            query_execute = self.db.execute(query)
            commit_changes = self.db.commit()
            result = asyncio.get_event_loop().run_until_complete(
                asyncio.gather(*[query_execute, commit_changes])
            )

            # Switch on job type.
            success = False
            match job_type:
                case JobType.Noop:
                    pass  # ?
                case JobType.BuildTopic:
                    raise Exception("Build topic job in wrong queue.")
                case JobType.CreateSearch:
                    (success, result) = self.search_handler.create_search(
                        queue_job
                    )
                case JobType.CreateDoccount:
                    (success, result) = self.concept_handler.create_doccount(
                        queue_job, self.database
                    )
                case _:
                    raise Exception(f"Unknown job type: {job_type}")
        except:
            # On exception, put queue_item on lost_and_found queue.
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.config.queue_host)
            )
            channel = connection.channel()
            channel.queue_declare(
                queue=self.config.queue_lost_and_found, durable=True
            )  # durable?
            channel.basic_qos(prefetch_count=1)
            channel.basic_publish(
                exchange="",
                routing_key=self.config.queue_lost_and_found,
                body=received,
            )
            connection.close()
        finally:
            # Update task in mongodb.
            db_task["status"]["state"] = JobState.Finished
            db_task["status"]["success"] = success
            db_task["status"]["is_finished"] = True
            db_task["finished"] = now()
            db_task["result"] = result

            updated_task = {"$set": db_task}
            result = self.databases.mongo_select(
                self.database
            ).tasks.update_one(task_filter, updated_task)

            ch.basic_ack(delivery_tag=method.delivery_tag)
