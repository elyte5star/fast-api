from pydantic import BaseModel, EmailStr
from modules.schemas.requests.base_request import RequestBase


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    telephone: str


class EditUser(BaseModel):
    username: str
    email: EmailStr
    password: str
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
