from pydantic import BaseModel, EmailStr
from .base_request import RequestBase


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    telephone: str


class CreateUserRequest(RequestBase):
    user: User


class GetUserRequest(RequestBase):
    userid: str = ""


class DeleteUserRequest(RequestBase):
    pass


class GetUsersRequest(RequestBase):
    pass
