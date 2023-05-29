from modules.schemas.requests.auth import (
    LoginDataRequest,
    RefreshTokenRequest,
    GoogleLoginDataRequest,
    LogOutRequest,
)
from modules.schemas.responses.auth import TokenResponse
from modules.database.models.user import _User
from modules.schemas.responses.base_response import BaseResponse
from modules.utils.base_functions import Utilities


class Auth(Utilities):
    async def authenticate_user(self, data: LoginDataRequest) -> TokenResponse:
        if await self.username_exist(data.username) is not None:
            async with self.get_session() as session:
                result = await session.execute(
                    self.select(_User).where(_User.username == data.username)
                )
                (user,) = result.first()
            if self.verify_password(data.password, user.password, self.cf.coding):
                active = True
                admin = False
                if user.username == self.cf.username:
                    admin = True
                data = {
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
                    data=data,
                    expires_delta=self.time_delta(self.cf.token_expire_min),
                )
                refresh_token = self.create_token(
                    data=data,
                    expires_delta=self.time_delta(self.cf.refresh_token_expire_minutes),
                )
                return TokenResponse(
                    token_data={
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "token_type": "bearer",
                        "host_url": self.cf.host_url,
                        "userid": user.userid,
                        "username": user.username,
                        "admin": admin,
                    },
                    message=f"User {user.username} is authorized!",
                )

            return TokenResponse(
                success=False,
                message=f"User {data.username} is not authorized.Incorrect password",
            )
        return TokenResponse(
            success=False,
            message=f"User {data.username} is not authorized.Incorrect username",
        )

    async def google_auth(self, data: GoogleLoginDataRequest) -> TokenResponse:
        pass

    async def refresh_token(self, payload: RefreshTokenRequest) -> TokenResponse:
        if (
            payload.token_load.username == self.cf.username
            and payload.data.type == self.cf.grant_type
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

            return TokenResponse(
                token_data={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_id": payload.token_load.token_id,
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
