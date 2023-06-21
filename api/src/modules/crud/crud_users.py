from modules.utils.base_functions import Utilities
from modules.schemas.requests.enquiry import Enquiry
from modules.schemas.requests.users import (
    CreateUserRequest,
    GetUserRequest,
    DeleteUserRequest,
)
from modules.schemas.responses.equiry import ClientEnquiryResponse
from fastapi.encoders import jsonable_encoder
from modules.schemas.responses.users import (
    CreateUserResponse,
    GetUsersResponse,
    GetUserResponse,
    BaseResponse,
    GetInfoResponse,
)
from sqlalchemy.sql.expression import false
from modules.database.models.user import _User
from modules.database.models.enquiry import _Enquiry
from sqlalchemy.orm import selectinload, defer
from typing import Optional
from modules.schemas.requests.auth import JWTcredentials


class Users(Utilities):
    async def _create_user(self, data: CreateUserRequest) -> CreateUserResponse:
        if (
            await self.username_email_exists(data.user.email, data.user.username)
            is None
        ):
            hashed_password = self.hash_password(
                data.user.password, self.cf.rounds, self.cf.coding
            )
            user_data_dict = data.user.dict()
            user_data_dict["userid"] = self.get_indent()
            user_data_dict["discount"] = None
            user_data_dict["password"] = hashed_password
            db_user = _User(**user_data_dict)
            async with self.get_session() as session:
                session.add(db_user)
                await session.commit()
                return CreateUserResponse(
                    userid=db_user.userid,
                    message=f"User with username {db_user.username} created!",
                )

        return BaseResponse(
            success=False,
            message="User already exist!",
        )

    async def _create_enquiry(self, data: Enquiry) -> ClientEnquiryResponse:
        client_equiry = _Enquiry(**data.dict(), eid=self._get_indent())
        async with self.get_session() as session:
            session.add(client_equiry)
            await session.commit()
            return ClientEnquiryResponse(
                eid=client_equiry.eid,
                message=f" Enquiry with {client_equiry.eid } created!",
            )

    async def _get_users(
        self,
    ) -> GetUsersResponse:
        async with self.get_session() as session:
            result = await session.execute(
                self.select(_User).options(
                    defer(_User.password), selectinload(_User.bookings)
                )
            )
            users = result.scalars().all()
            if len(users) > 0:
                return GetUsersResponse(
                    users=users, message=f"Total number of users: {len(users)}"
                )
            return BaseResponse(
                success=False,
                message="Users not found!!",
            )

    async def get_info(self, credentials: JWTcredentials) -> GetInfoResponse:
        if credentials.username == self.cf.username:
            async with self.get_session() as _:
                _, kwargs = self._engine.dialect.create_connect_args(self._engine.url)
            return GetInfoResponse(info=kwargs, message="Database Url")
        return GetInfoResponse(success=False, message="Admin rights needed!")

    async def _get_user(self, data: GetUserRequest) -> GetUserResponse:
        if await self.userid_exist(data.userid) is not None:
            async with self.get_session() as session:
                result = await session.execute(
                    self.select(_User)
                    .where(_User.userid == data.userid)
                    .options(defer(_User.password), selectinload(_User.bookings))
                )

                (user,) = result.first()

                return GetUserResponse(
                    user=user,
                    message=f"User with id:{data.userid} found!",
                )
        return BaseResponse(
            success=False,
            message=f"User with id:{data.userid} not found!!",
        )

    async def _delete_user(self, data: DeleteUserRequest) -> BaseResponse:
        if await self.userid_exist(data.userid) is not None:
            async with self.get_session() as session:
                await session.execute(
                    self.delete(_User).where(_User.userid == data.userid)
                )
                await session.commit()
                return BaseResponse(
                    message=f"User with id:{data.userid} deleted",
                )

        return BaseResponse(
            success=False,
            message=f"User with id:{data.userid} doesnt exist!",
        )
