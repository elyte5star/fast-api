from pydantic import BaseModel, EmailStr, SecretStr
from modules.schemas.requests.base_request import RequestBase
from typing import Any


class User(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
    telephone: str
    active: bool = False


class EmailSchema(BaseModel):
    email: list[EmailStr]
    body: dict[str, Any]


class EditUser(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
    telephone: str


class CreateUserRequest(RequestBase):
    user: User


class UpdateUserRequest(RequestBase):
    user: EditUser


class GetUserRequest(RequestBase):
    userid: str = ""


class DeleteUserRequest(RequestBase):
    pass


class GetUsersRequest(RequestBase):
    pass
