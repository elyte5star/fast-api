from modules.schemas.requests.auth import (
    LoginDataRequest,
    RefreshTokenRequest,
    GoogleLoginDataRequest,
    JWTcredentials,
    BlackListRequest,
)
from modules.schemas.responses.auth import TokenResponse
from modules.database.models.user import _User
from modules.schemas.responses.base_response import BaseResponse
from modules.database.models.blacklist import _BlackList
from .blacklist import BlackListHandler


class Auth(BlackListHandler):
    async def authenticate_user(self, data: LoginDataRequest) -> TokenResponse:
        users = await self.execute(
            self.select(_User).where(_User.username == data.username)
        )
        (user,) = users.first()
        if user and self.verify_password(data.password, user.password, self.cf.coding):
            active = True
            admin = False
            if user.username == self.cf.username:
                admin = True
            token_data = {
                "userid": user.userid,
                "sub": user.username,
                "email": user.email,
                "admin": admin,
                "active": active,
                "discount": user.discount,
                "telephone": user.telephone,
                "token_id": self.get_indent(),
            }
            access_token = self.create_token(
                data=token_data,
                expires_delta=self.time_delta(self.cf.token_expire_min),
            )
            refresh_token = self.create_token(
                data=token_data,
                expires_delta=self.time_delta(self.cf.refresh_token_expire_minutes),
            )

            blacklist_orm_data = BlackListRequest(
                token_id=token_data["token_id"], token=access_token
            )
            if await self.create_blacklist(blacklist_orm_data):
                return TokenResponse(
                    token_data={
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "token_id": blacklist_orm_data.token_id,
                        "token_type": "bearer",
                        "host_url": self.cf.host_url,
                        "email": user.email,
                        "userid": user.userid,
                        "username": user.username,
                        "admin": admin,
                    },
                    message=f"User {user.username} is authorized:Blacklist created!",
                )
        return TokenResponse(
            success=False,
            message=f"User {user.username} is not authorized.Incorrect username or password",
        )

    async def google_auth(self, data: GoogleLoginDataRequest) -> TokenResponse:
        query = self.select(_User).where(_User.email == data.google_data.email)
        users = await self.execute(query)
        (user,) = users.first()
        pass

    async def _logout(self, data: JWTcredentials):
        if await self.blacklist_token(data.token_id):
            return BaseResponse(
                message=f" user token id: {data.token_id} added to blacklist"
            )
        return BaseResponse(message="Bad Operation", success=False)

    async def refresh_token(self, payload: RefreshTokenRequest) -> TokenResponse:
        if (
            payload.token_load.username == self.cf.username
            and payload.data.type == self.cf.grant_type
            and await self.blacklist_token(payload.data.old_token_id)
        ):
            payload.token_load.token_id = self.get_indent()
            data_dict = payload.token_load.dict()
            data_dict["sub"] = data_dict.pop("username")
            access_token = self.create_token(
                data=data_dict,
                expires_delta=self.time_delta(self.cf.token_expire_min),
            )
            refresh_token = self.create_token(
                data=data_dict,
                expires_delta=self.time_delta(self.cf.refresh_token_expire_minutes),
            )
            blacklist_orm_data = _BlackList(
                token_id=payload.token_load.token_id,
                token=access_token,
                active=True,
            )
            if await self.create_blacklist(blacklist_orm_data):
                return TokenResponse(
                    token_data={
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "token_id": blacklist_orm_data.token_id,
                        "token_type": "bearer",
                        "host_url": self.cf.host_url,
                        "userid": payload.token_load.userid,
                        "username": payload.token_load.username,
                        "admin": payload.token_load.admin,
                    },
                    message="Fresh token created : Blacklist created!",
                )

        return TokenResponse(
            success=False,
            message="Couldnt refresh token.",
        )
