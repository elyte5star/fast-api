from datetime import datetime, timedelta
import time
import numpy as np
import string, random
import bcrypt
from jose import jwt
from typing import Optional
import uuid
from modules.database.db_session import AsyncDatabaseSession
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi_mail.errors import ConnectionErrors
from modules.schemas.requests.users import EmailSchema


class Utilities(AsyncDatabaseSession):
    def return_config_object(self):
        return self.cf

    def obj_as_json(self, obj):
        return jsonable_encoder(obj)

    def generate_confirmation_token(self, email: EmailStr):
        serializer = URLSafeTimedSerializer(
            self.cf.secret_key, salt=self.cf.security_salt
        )
        return serializer.dumps(email)

    async def send_with_template(
        self, data: EmailSchema, subject: str, template_file: str
    ) -> bool:
        message = MessageSchema(
            subject=subject,
            recipients=data.dict().get("email"),
            template_body=data.dict().get("body"),
            subtype=MessageType.html,
        )
        fm = FastMail(self.cf.email_config)
        try:
            await fm.send_message(message, template_name=template_file)
            return True
        except ConnectionErrors as e:
            self.log.error(e)
            return False

    def verify_email_token(self, token: str, expiration: int = 3600):
        serializer = URLSafeTimedSerializer(self.cf.secret_key)
        try:
            email = serializer.loads(
                token, salt=self.cf.security_salt, max_age=expiration
            )
            return {"email": email, "check": True}
        except SignatureExpired:
            return None
        except BadTimeSignature:
            return None

    def time_now(self) -> datetime:
        return datetime.utcnow()

    def time_then(self) -> datetime:
        return datetime(1980, 1, 1)

    def get_user_string(self, string_length: int = 10) -> str:
        letters = string.ascii_lowercase + "0123456789" + string.ascii_uppercase
        return "".join(random.choice(letters) for _ in range(string_length))

    def _get_indent(self, size: int = 12):
        chars = string.digits
        return "".join(random.choice(chars) for _ in range(size))

    def _get_x_correlation_id(self):
        size = 12
        chars = string.digits
        correlation_id = "".join(random.choice(chars) for _ in range(size)) + "_SC"
        return correlation_id

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

    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        _encode = data.copy()
        if expires_delta:
            _expire = self.time_now() + expires_delta
        else:
            _expire = self.time_now() + self.time_delta(self.cf.token_expire_min)
        _encode.update({"exp": _expire})
        jwt_encode = jwt.encode(
            _encode, self.cf.secret_key, algorithm=self.cf.algorithm
        )
        return jwt_encode
