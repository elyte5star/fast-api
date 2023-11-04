from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from modules.schemas.responses.auth import (
    TokenResponse,
    BaseResponse,
)
from modules.schemas.requests.auth import LoginData, CloudLoginData
from modules.auth.dependency import security
from modules.schemas.requests.users import EmailSchema


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    summary="Get token",
    response_model=TokenResponse,
)
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
    "/get-token",
    response_model=TokenResponse,
    summary="Get token for Cloud users",
)
async def get_token(data: CloudLoginData):
    return await handler._get_token(
        CloudLoginData(
            token=data.token,
            type=data.type,
        )
    )


@router.get(
    "/confirm-email/{token}", response_model=BaseResponse, summary="Confirm Email Token"
)
async def confirm_email_token(token: str) -> BaseResponse:
    return await handler.confirm_email_token(token)


@router.post(
    "/send-email-confirmation",
    response_model=BaseResponse,
    summary="Send Confirmation Email",
)
async def confirm_email(data: EmailSchema) -> BaseResponse:
    return await handler.send_email_confirmation(data)
