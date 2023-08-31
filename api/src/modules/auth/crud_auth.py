from modules.schemas.requests.auth import (
    LoginData,
    CloudLoginData,
    LogOutRequest,
)
from modules.schemas.responses.auth import (
    TokenResponse,
    BaseResponse,
)
from modules.database.models.user import _User
from modules.utils.base_functions import Utilities
from sqlalchemy.sql.expression import false
from sqlalchemy.orm import selectinload, defer
from modules.schemas.requests.users import EmailSchema


class Auth(Utilities):
    async def authenticate_user(self, data: LoginData) -> TokenResponse:
        if await self.username_exist(data.username) is not None:
            async with self.get_session() as session:
                result = await session.execute(
                    self.select(_User).where(_User.username == data.username)
                )
                (user,) = result.first()
            if user.active == false():
                return TokenResponse(
                    token_data={
                        "active": user.active,
                        "userid": user.userid,
                        "username": user.username,
                        "email": user.email,
                    },
                    success=False,
                    message="Account Not Verified",
                )

            if self.verify_password(
                data.password.get_secret_value(), user.password, self.cf.coding
            ):
                admin = False
                if user.username == self.cf.username:
                    admin = True
                data = {
                    "userid": user.userid,
                    "sub": user.username,
                    "email": user.email,
                    "admin": admin,
                    "active": user.active,
                    "discount": user.discount,
                    "telephone": user.telephone,
                    "token_id": self.get_indent(),
                }
                access_token = self.create_token(
                    data=data,
                    expires_delta=self.time_delta(self.cf.token_expire_min),
                )

                return TokenResponse(
                    token_data={
                        "access_token": access_token,
                        "token_type": "bearer",
                        "host_url": self.cf.host_url,
                        "userid": user.userid,
                        "active": user.active,
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
            message=f"User {data.username} is not authorized. Incorrect username/User not found!",
        )

    async def _get_token(self, data: CloudLoginData) -> TokenResponse:
        active = True
        admin = False
        discount = None
        username = "_".join(data.username.split()).lower()
        if username == self.cf.username:
            admin = True
        _data = {
            "userid": data.userid,
            "sub": username,
            "email": data.email,
            "admin": admin,
            "active": active,
            "discount": discount,
            "telephone": "",
            "token_id": self._get_indent(),
        }

        access_token = self.create_token(
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
                "token_type": "bearer",
                "host_url": self.cf.host_url,
                "userid": data.userid,
                "username": username,
                "admin": admin,
            },
            message=f"User {data.username} is authorized!",
        )

    async def confirm_email_token(self, token: str):
        token_data = self.verify_email_token(token)
        if token_data is None:
            return BaseResponse(
                message="The confirmation link is invalid or has expired.",
                success=False,
            )
        if await self.useremail_exist(token_data["email"]) is not None:
            async with self.get_session() as session:
                result = await session.execute(
                    self.select(_User).where(_User.email == token_data["email"])
                )
                (user,) = result.first()

            if user.active:
                return BaseResponse(message="Account already confirmed. Please login.")
            else:
                async with self.get_session() as session:
                    await session.execute(
                        self.update(_User)
                        .where(_User.email == token_data["email"])
                        .values(dict(active=True))
                        .execution_options(synchronize_session="fetch")
                    )
                    await session.commit()
                    return BaseResponse(message="Email Verification Successful")
        return BaseResponse(
            message=f"User with email {token_data['email']} does not exist",
            success=False,
        )

    async def send_email_confirmation(self, data: EmailSchema):
        if await self.useremail_exist(data.email[0]) is not None:
            token = self.generate_confirmation_token(data.email[0])
            data.body["token"] = token
            mail_status = await self.send_with_template(
                data, "Confirm Your Email", "verify_email.html"
            )
            if mail_status:
                return BaseResponse(
                    message=f"Email confirmation sent for userid : {data.body['username']} !",
                )
        return BaseResponse(
            message=f"User with email {data.email[0]} does not exist",
            success=False,
        )
