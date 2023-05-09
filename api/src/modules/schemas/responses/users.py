from pydantic import BaseModel, SecretStr, EmailStr
from pydantic.types import Any
from .base_response import BaseResponse
from datetime import datetime


class User(BaseModel):
    username: str
    password: SecretStr
    userid: str
    email: EmailStr
    active: bool = True
    discount: float = 0.0
    telephone: int = 0
    created_at: datetime = datetime.utcnow


class CreateUserResponse(BaseResponse):
    userid: str = ""


class GetUserResponse(BaseResponse):
    user: Any = {}


class GetUsersResponse(BaseResponse):
    users: list = []


class UserInDb(BaseResponse):
    hashed_password: str = ""
