
from enum import Enum
from pydantic import BaseModel



class JobType(str,Enum):
    Noop = '0'
    CreateSearch = '10'
    CreateBooking = '30'
    


class JobState(str,Enum):
    NotSet = '0'
    Received = '10'
    Pending = '20'
    Finished = '30'
    Timeout = '666'
    NoTasks = '999'


class JobStatus(BaseModel):
    state: JobState = JobState.NotSet
    success: bool = False
    is_finished: bool = False