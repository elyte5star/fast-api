from fastapi import APIRouter, Depends
from resources.schemas.requests.users import (
    CreateUserRequest,
    GetUserRequest,
    DeleteUserRequest,
    User,
)
from resources.schemas.responses.base_response import BaseResponse
from resources.schemas.responses.users import (
    CreateUserResponse,
    GetUsersResponse,
    GetUserResponse,
)
from resources.schemas.requests.auth import JWTcredentials
from resources.auth.dependency import security


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/signup", response_model=CreateUserResponse, summary="Create User"
)
async def create_user(user_data: User) -> CreateUserResponse:
    return await handler._create_user(CreateUserRequest(user=user_data))


@router.get("/all", response_model=GetUsersResponse, summary="Get all Users")
async def get_users(
    cred: JWTcredentials = Depends(security),
) -> GetUsersResponse:
    return await handler._get_users()


@router.get(
    "/{userid}", response_model=GetUserResponse, summary="Get one user"
)
async def get_user(
    userid: str, cred: JWTcredentials = Depends(security)
) -> GetUserResponse:
    return await handler._get_user(GetUserRequest(userid=userid))


@router.delete(
    "/{userid}", response_model=BaseResponse, summary="Delete a user"
)
async def delete_user(
    userid: str, cred: JWTcredentials = Depends(security)
) -> BaseResponse:
    return await handler._delete_user(DeleteUserRequest(userid=userid))
