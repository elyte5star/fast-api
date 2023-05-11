from fastapi import APIRouter, Depends
from starlette.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from modules.schemas.responses.auth import TokenResponse
from starlette.requests import Request
from modules.schemas.responses.base_response import BaseResponse
from modules.schemas.requests.auth import (
    JWTcredentials,
    RefreshTokenRequest,
    LoginDataRequest,
    GrantType,
    GoogleLoginDataRequest,
    GoogleLoginData,
    LogOutRequest,
)
from modules.auth.dependency import security

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", summary="Get token", response_model=TokenResponse)
async def token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenResponse:
    return await handler.authenticate_user(
        LoginDataRequest(
            request=request,
            username=form_data.username,
            password=form_data.password,
        )
    )


@router.get("/logout")
async def logout(cred: JWTcredentials = Depends(security)):
    return await handler._logout(LogOutRequest(token_load=cred))


@router.post("/refresh_token", response_model=TokenResponse, summary="Refresh token")
async def refresh_token(
    request: Request, data: GrantType, cred: JWTcredentials = Depends(security)
) -> TokenResponse:
    return await handler.refresh_token(RefreshTokenRequest(data=data, token_load=cred))


@router.post(
    "/google",
    summary="Get token for Google user",
    response_model=TokenResponse,
)
async def google_token(request: Request, data: GoogleLoginData) -> TokenResponse:
    return await handler.google_auth(
        GoogleLoginDataRequest(request=request, google_data=data)
    )
