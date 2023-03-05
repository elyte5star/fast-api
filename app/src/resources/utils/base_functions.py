from datetime import datetime, timedelta
import time
import numpy as np
import string, random
import bcrypt
from jose import jwt
from typing import Optional
import uuid
from resources.database.db_session import AsyncDatabaseSession


class Utilities(AsyncDatabaseSession):
    def return_config_object(self):
        return self.cf

    def time_now(self) -> datetime:
        return datetime.utcnow()

    def time_then(self) -> datetime:
        return datetime.datetime(1980, 1, 1)

    def get_user_string(self, stringLength: int = 10) -> str:
        letters = (
            string.ascii_lowercase + "0123456789" + string.ascii_uppercase
        )
        return "".join(random.choice(letters) for i in range(stringLength))

    def get_indent(self):
        return str(uuid.uuid4())

    def time_delta(self, min: int) -> timedelta:
        return timedelta(minutes=min)

    def hash_password(self, password: str, rounds: int, coding: str) -> str:
        hashed_password = bcrypt.hashpw(
            password.encode(coding), bcrypt.gensalt(rounds=rounds)
        ).decode(coding)
        return hashed_password

    def verify_password(
        self, plain_password: str, hashed_password: str, coding: str
    ) -> bool:
        if bcrypt.checkpw(
            plain_password.encode(coding), hashed_password.encode(coding)
        ):
            return True
        return False

    def random_date(self, start_date, range_in_days):
        days_to_add = np.arange(0, range_in_days)
        rd = np.datetime64(start_date) + np.random.choice(days_to_add)
        return str(rd)

    def create_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        _encode = data.copy()
        if expires_delta:
            _expire = self.time_now() + expires_delta
        else:
            _expire = self.time_now() + self.time_delta(
                self.cf.token_expire_min
            )
        _encode.update({"exp": _expire})
        jwt_encode = jwt.encode(
            _encode, self.cf.secret_key, algorithm=self.cf.algorithm
        )
        return jwt_encode
