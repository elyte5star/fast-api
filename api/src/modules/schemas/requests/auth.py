from pydantic import BaseModel
from datetime import timedelta
from typing import Optional
from .base_request import RequestBase


class GrantType(BaseModel):
    type: str = ""
    old_token_id: str = ""


class LoginData(BaseModel):
    username: str
    password: str


class CloudLoginData(BaseModel):
    username: str
    email: str
    userid: str


class JWTcredentials(BaseModel):
    userid: str
    email: str
    username: str
    admin: bool
    active: bool
    exp: timedelta
    token_id: str
    discount: Optional[float] = None
    telephone: Optional[str] = None


class RefreshTokenRequest(RequestBase):
    data: GrantType


class LogOutRequest(BaseModel):
    token_load: JWTcredentials


class BlackListRequest(BaseModel):
    token_id: str
    token: str
