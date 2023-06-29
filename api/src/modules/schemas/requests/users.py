from pydantic import BaseModel, EmailStr
from .base_request import RequestBase
from typing import Optional


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    telephone: str


class EditUser(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str] = None  # or Union[str, None]
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
