from pydantic import BaseModel
from datetime import timedelta
from typing import Optional
from .base_request import RequestBase


class GrantType(BaseModel):
    type: str = ""
    old_token_id: str = ""


class LoginDataRequest(RequestBase):
    username: str
    password: str


class GoogleLoginData(BaseModel):
    username: str
    email: str


class GoogleLoginDataRequest(RequestBase):
    google_data = GoogleLoginData


class JWTcredentials(BaseModel):
    userid: str
    email: str
    username: str
    admin: bool
    active: bool
    exp: timedelta
    token_id: str
    discount: Optional[float] = None
    telephone: int


class RefreshTokenRequest(RequestBase):
    data: GrantType = None


class LogOutRequest(BaseModel):
    token_load: JWTcredentials


class BlackListRequest(BaseModel):
    token_id:str
    token:str
