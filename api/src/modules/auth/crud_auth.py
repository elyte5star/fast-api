from modules.schemas.requests.auth import (
    LoginDataRequest,
    RefreshTokenRequest,
    GoogleLoginDataRequest,
)
from modules.schemas.responses.auth import TokenResponse
from modules.database.models.user import User
from starlette.responses import RedirectResponse
from modules.schemas.responses.base_response import BaseResponse
from modules.database.models.blacklist import BlackList
from .blacklist import BlackListHandler


class Auth(BlackListHandler):
    async def authenticate_user(self, data: LoginDataRequest) -> TokenResponse:
        query = self.select(User).where(User.username == data.username)
        users = await self.execute(query)
        (user,) = users.first()
        if user and self.verify_password(
            data.password, user.password, self.cf.coding
        ):
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
                expires_delta=self.time_delta(
                    self.cf.refresh_token_expire_minutes
                ),
            )

            blacklist_orm_data = BlackList(
                token_id=token_data["token_id"], token=access_token
            )
            if await self.create_blacklist(blacklist_orm_data):
                data.request.session["user"] = token_data
                return TokenResponse(
                    token_data={
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "token_id": blacklist_orm_data.token_id,
                        "token_type": "bearer",
                        "host_url": self.cf.host_url,
                        "userid": user.userid,
                    },
                    message=f"User {user.username} is authorized:Blacklist created!",
                )
        return TokenResponse(
            success=False,
            message=f"User {user.username} is not authorized.Incorrect username or password",
        )

    async def google_auth(self, data: GoogleLoginDataRequest) -> TokenResponse:
        query = self.select(User).where(User.email == data.google_data.email)
        users = await self.execute(query)
        (user,) = users.first()
        if user:
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
                expires_delta=self.time_delta(
                    self.cf.refresh_token_expire_minutes
                ),
            )

            blacklist_orm_data = BlackList(
                token_id=token_data["token_id"], token=access_token
            )
            if await self.create_blacklist(blacklist_orm_data):
                data.request.session["user"] = token_data
                return TokenResponse(
                    token_data={
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "token_id": blacklist_orm_data.token_id,
                        "token_type": "bearer",
                        "host_url": self.cf.host_url,
                        "userid": user.userid,
                    },
                    message=f"User {user.username} is authorized:Blacklist created!",
                )
        return TokenResponse(
            success=False,
            message=f"User {user.username} is not authorized.Incorrect username or password",
        )

    async def _logout(self, cred, request):
        request.session.pop("user", None)
        if await self.blacklist_token(cred.token_id):
            return BaseResponse(
                message=f" user token id: {cred.token_id} added to blacklist"
            )
        return BaseResponse(message="Bad Operation", success=False)

    async def refresh_token(
        self, payload: RefreshTokenRequest
    ) -> TokenResponse:

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
                expires_delta=self.time_delta(
                    self.cf.refresh_token_expire_minutes
                ),
            )
            blacklist_orm_data = BlackList(
                token_id=payload.token_load.token_id,
                token=access_token,
                active=True,
            )
            if await self.create_blacklist(blacklist_orm_data):
                payload.request.session["user"] = data_dict
                return TokenResponse(
                    token_data={
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "token_id": blacklist_orm_data.token_id,
                        "token_type": "bearer",
                        "host_url": self.cf.host_url,
                        "userid": payload.token_load.userid,
                    },
                    message="Fresh token created : Blacklist created!",
                )

        return TokenResponse(
            success=False,
            message="Couldnt refresh token.",
        )
