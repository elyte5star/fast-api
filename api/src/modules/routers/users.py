from fastapi import APIRouter, Depends
from modules.schemas.requests.users import (
    CreateUserRequest,
    GetUserRequest,
    DeleteUserRequest,
    User,
    EditUser,
    UpdateUserRequest,
    
)
from modules.schemas.requests.enquiry import Enquiry
from modules.schemas.responses.base_response import BaseResponse
from modules.schemas.responses.users import (
    CreateUserResponse,
    GetUsersResponse,
    GetUserResponse,
    GetInfoResponse,
)
from modules.schemas.responses.enquiry import ClientEnquiryResponse
from modules.schemas.requests.auth import JWTcredentials
from modules.auth.dependency import security


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup", response_model=CreateUserResponse, summary="Create User")
async def create_user(user_data: User) -> CreateUserResponse:
    return await handler._create_user(CreateUserRequest(user=user_data))



@router.post(
    "/customer/service",
    response_model=ClientEnquiryResponse,
    summary="Customer Service",
)
async def create_enquiry(enquiry: Enquiry) -> ClientEnquiryResponse:
    return await handler._create_enquiry(enquiry)


@router.get("", response_model=GetUsersResponse, summary="Get all Users")
async def get_users(
    cred: JWTcredentials = Depends(security),
) -> GetUsersResponse:
    return await handler._get_users(cred)


@router.put("/{userid}", response_model=CreateUserResponse, summary="Update User")
async def update_user(userid: str, user_data: EditUser) -> CreateUserResponse:
    return await handler._update_user(UpdateUserRequest(user=user_data, userid=userid))


@router.get("/{userid}", response_model=GetUserResponse, summary="Get one user")
async def get_user(
    userid: str, cred: JWTcredentials = Depends(security)
) -> GetUserResponse:
    return await handler._get_user(GetUserRequest(userid=userid))


@router.get("/admin/info", response_model=GetInfoResponse, summary="System Information")
async def db_info(cred: JWTcredentials = Depends(security)) -> GetInfoResponse:
    return await handler.get_info(cred)


@router.delete("/{userid}", response_model=BaseResponse, summary="Delete a user")
async def delete_user(
    userid: str, cred: JWTcredentials = Depends(security)
) -> BaseResponse:
    return await handler._delete_user(DeleteUserRequest(userid=userid))
