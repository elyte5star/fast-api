from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from modules.schemas.responses.auth import TokenResponse
from starlette.requests import Request
from modules.schemas.requests.auth import (
    JWTcredentials,
    RefreshTokenRequest,
    LoginDataRequest,
    GrantType,
    GoogleLoginDataRequest,
    GoogleLoginData,
    
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
