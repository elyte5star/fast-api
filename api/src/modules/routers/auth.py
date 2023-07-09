from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from modules.schemas.responses.auth import TokenResponse
from starlette.requests import Request
from modules.schemas.requests.auth import (
    LoginData,
    CloudLoginData,
)
from modules.auth.dependency import security

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", summary="Get token", response_model=TokenResponse)
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenResponse:
    return await handler.authenticate_user(
        LoginData(
            username=form_data.username,
            password=form_data.password,
        )
    )


@router.post(
    "/get_token",
    response_model=TokenResponse,
    summary="Get token for Cloud users",
)
async def get_token(data: CloudLoginData):
    return await handler._get_token(
        CloudLoginData(username=data.username, email=data.email, userid=data.userid)
    )
