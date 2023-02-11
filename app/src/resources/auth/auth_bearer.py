import time
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from resources.schemas.requests.auth import JWTcredentials
from resources.settings.config import Settings
from .blacklist import BlackListHandler

# https://testdriven.io/blog/fastapi-jwt-auth/

cf = Settings().from_toml_file()

black_list = BlackListHandler(cf)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                request.session.pop("user", None)
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            if self.verify_jwt(credentials.credentials) is None:
                request.session.pop("user", None)
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            if await black_list.is_token_blacklisted(self.payload["token_id"]):
                request.session.pop("user", None)
                raise HTTPException(
                    status_code=403, detail="Invalid token.Token in blacklist"
                )
            _credentials = JWTcredentials(
                userid=self.payload["userid"],
                email=self.payload["email"],
                username=self.payload["sub"],
                active=self.payload["active"],
                exp=self.payload["exp"],
                admin=self.payload["admin"],
                token_id=self.payload["token_id"],
                discount=self.payload["discount"],
                telephone=self.payload["telephone"],
            )
            return _credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code."
            )

    def verify_jwt(self, token: str):
        if token is None:
            return None
        try:
            self.payload = jwt.decode(
                token, cf.secret_key, algorithms=[cf.algorithm]
            )
            return self.payload if self.payload["exp"] >= time.time() else None
        except JWTError:
            return None
