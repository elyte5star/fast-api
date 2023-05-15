from modules.utils.base_functions import Utilities
from modules.schemas.requests.users import (
    CreateUserRequest,
    GetUserRequest,
    DeleteUserRequest,
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from modules.schemas.responses.users import (
    CreateUserResponse,
    GetUsersResponse,
    GetUserResponse,
    BaseResponse,
)
from sqlalchemy.sql.expression import false
from modules.database.models.user import _User
from sqlalchemy.orm import selectinload, defer


class Users(Utilities):
    async def _create_user(self, data: CreateUserRequest) -> CreateUserResponse:
        hashed_password = self.hash_password(
            data.user.password, self.cf.rounds, self.cf.coding
        )
        user_data_dict = data.user.dict()
        user_data_dict["userid"] = self.get_indent()
        user_data_dict["discount"] = None
        user_data_dict["password"] = hashed_password
        db_user = _User(**user_data_dict)
        self.add(db_user)
        try:
            await self.commit()
            return CreateUserResponse(
                userid=db_user.userid,
                message=f"User with username {db_user.username} created!",
            )
        except IntegrityError as e:
            self.log.warning(e)
            await self.rollback()
            return BaseResponse(
                success=False,
                message=str(e),
            )

    def is_active(self, user: _User) -> bool:
        return False if user.active == false() else True

    def is_admin(self, user: _User) -> bool:
        return False if user.admin == false() else True

    async def _get_users(
        self,
    ) -> GetUsersResponse:
        result = await self.execute(
            self.select(_User).options(
                defer(_User.password), selectinload(_User.bookings)
            )
        )
        if result is not None:
            users = result.scalars().all()
            return GetUsersResponse(
                users=users, message=f"Total number of users: {len(users)}"
            )
        else:
            return BaseResponse(
                success=False,
                message="Users not found!!",
            )

    async def _get_user(self, data: GetUserRequest) -> GetUserResponse:
        result = await self.execute(
            self.select(_User)
            .where(_User.userid == data.userid)
            .options(defer(_User.password), selectinload(_User.bookings))
        )
        if data and result is not None:
            (user,) = result.first()
            return GetUserResponse(
                user=user,
                message=f"User with id:{data.userid} found!",
            )
        else:
            return BaseResponse(
                success=False,
                message=f"User with id:{data.userid} not found!!",
            )

    async def _delete_user(self, data: DeleteUserRequest) -> BaseResponse:
        query = self.delete(_User).where(_User.userid == data.userid)
        await self.execute(query)
        try:
            await self.commit()
            return BaseResponse(
                message=f"User with id:{data.userid} deleted",
            )
        except IntegrityError as e:
            self.log.info(e)
            await self.rollback()
            return BaseResponse(
                success=False,
                message=f"Deletion not successful for user with id:{data.userid}",
            )
