from modules.schemas.requests.auth import (
    LoginData,
    CloudLoginData,
    LogOutRequest,
)
from modules.schemas.responses.auth import TokenResponse
from modules.database.models.user import _User
from modules.utils.base_functions import Utilities


class Auth(Utilities):
    async def authenticate_user(self, data: LoginData) -> TokenResponse:
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

    async def _get_token(self, data: CloudLoginData) -> TokenResponse:
        active = True
        admin = False
        discount = None
        if data.username == self.cf.username:
            admin = True
        _data = {
            "userid": data.userid,
            "sub": data.username,
            "email": data.email,
            "admin": admin,
            "active": active,
            "discount": discount,
            "telephone": "",
            "token_id": self._get_indent(),
        }

        access_token = self.create_token(
            data=_data,
            expires_delta=self.time_delta(self.cf.token_expire_min),
        )
        refresh_token = self.create_token(
            data=_data,
            expires_delta=self.time_delta(self.cf.refresh_token_expire_minutes),
        )
        if await self.userid_exist(data.userid) is None:
            _data.pop("token_id")
            _data["username"] = _data.pop("sub")

            _data["password"] = self.hash_password(
                "valid_cloud_user", self.cf.rounds, self.cf.coding
            )
            db_user = _User(**_data)
            async with self.get_session() as session:
                session.add(db_user)
                await session.commit()
            self.log.info("A new user account created!")
        return TokenResponse(
            token_data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "host_url": self.cf.host_url,
                "userid": data.userid,
                "username": data.username,
                "admin": admin,
            },
            message=f"User {data.username} is authorized!",
        )
