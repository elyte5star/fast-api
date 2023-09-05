from datetime import datetime, timedelta
import time
import numpy as np
import string, random, json, base64
import bcrypt
from jose import jwt
from typing import Optional
import uuid
from modules.database.db_session import AsyncDatabaseSession
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi_mail.errors import ConnectionErrors
from modules.schemas.requests.users import EmailSchema
from google.oauth2 import id_token
from google.auth.transport import requests


class Utilities(AsyncDatabaseSession):
    def serialize_datetime(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")

    def return_config_object(self):
        return self.cf

    def obj_as_json(self, obj):
        return jsonable_encoder(obj)

    def generate_confirmation_token(self, email: EmailStr):
        serializer = URLSafeTimedSerializer(
            self.cf.secret_key, salt=self.cf.security_salt
        )
        return serializer.dumps(email)

    async def send_with_template(
        self, data: EmailSchema, subject: str, template_file: str
    ) -> bool:
        message = MessageSchema(
            subject=subject,
            recipients=data.dict().get("email"),
            template_body=data.dict().get("body"),
            subtype=MessageType.html,
        )
        fm = FastMail(self.cf.email_config)
        try:
            await fm.send_message(message, template_name=template_file)
            return True
        except ConnectionErrors as e:
            self.log.error(e)
            return False

    def decode_msal_id_token_part(self, raw, encoding="utf-8"):
        """Decode a part of the JWT.

        JWT is encoded by padding-less base64url,
        based on `JWS specs <https://tools.ietf.org/html/rfc7515#appendix-C>`_.

        :param encoding:
            If you are going to decode the first 2 parts of a JWT, i.e. the header
            or the payload, the default value "utf-8" would work fine.
            If you are going to decode the last part i.e. the signature part,
            it is a binary string so you should use `None` as encoding here.
        """
        raw += "=" * (-len(raw) % 4)  # https://stackoverflow.com/a/32517907/728675
        raw = str(
            # On Python 2.7, argument of urlsafe_b64decode must be str, not unicode.
            # This is not required on Python 3.
            raw
        )
        output = base64.urlsafe_b64decode(raw)
        if encoding:
            output = output.decode(encoding)
        return output

    def decode_msal_id_token(
        self, id_token, client_id=None, issuer=None, nonce=None, now=None
    ):
        """Decodes and validates an id_token and returns its claims as a dictionary.

        ID token claims would at least contain: "iss", "sub", "aud", "exp", "iat",
        per `specs <https://openid.net/specs/openid-connect-core-1_0.html#IDToken>`_
        and it may contain other optional content such as "preferred_username",
        `maybe more <https://openid.net/specs/openid-connect-core-1_0.html#Claims>`_
        """
        decoded = json.loads(self.decode_msal_id_token_part(id_token.split(".")[1]))
        err = None  # https://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation
        _now = now or time.time()
        skew = 120  # 2 minutes
        if _now + skew < decoded.get("nbf", _now - 1):  # nbf is optional per JWT specs
            # This is not an ID token validation, but a JWT validation
            # https://tools.ietf.org/html/rfc7519#section-4.1.5
            err = "0. The ID token is not yet valid"
        if issuer and issuer != decoded["iss"]:
            # https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfigurationResponse
            err = (
                '2. The Issuer Identifier for the OpenID Provider, "%s", '
                "(which is typically obtained during Discovery), "
                "MUST exactly match the value of the iss (issuer) Claim."
            ) % issuer
        if client_id:
            valid_aud = (
                client_id in decoded["aud"]
                if isinstance(decoded["aud"], list)
                else client_id == decoded["aud"]
            )
            if not valid_aud:
                err = (
                    "3. The aud (audience) Claim must contain this client's client_id."
                )
        # Per specs:
        # 6. If the ID Token is received via direct communication between
        # the Client and the Token Endpoint (which it is in this flow),
        # the TLS server validation MAY be used to validate the issuer
        # in place of checking the token signature.
        if _now > decoded["exp"]:
            err = "9. The current time MUST be before the time represented by the exp Claim."
        if nonce and nonce != decoded.get("nonce"):
            err = (
                "11. Nonce must be the same value "
                "as the one that was sent in the Authentication Request"
            )
        if err:
            raise RuntimeError(
                "%s id_token was: %s" % (err, json.dumps(decoded, indent=2))
            )
        return decoded

    def verify_msal_jwt(self, token: str) -> dict | None:
        if token is None:
            return None
        try:
            token_claims = self.decode_msal_id_token(
                token, self.cf.msal_client_id, self.cf.msal_issuer
            )
            response_data = {
                "userid": token_claims["oid"],
                "sub": token_claims["name"],
                "email": token_claims["preferred_username"],
            }
            return response_data

        except Exception as err:
            print(err)
            return None

    def verify_gmail_jwt(self, token: str) -> dict | None:
        if token is None:
            return None
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            token_claims = id_token.verify_oauth2_token(
                token, requests.Request(), self.cf.google_client_id
            )
            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            response_data = {
                "userid": token_claims["sub"],
                "sub": token_claims["name"],
                "email": token_claims["email"],
            }

            return response_data
        except ValueError:
            return None

    def verify_email_token(self, token: str, expiration: int = 3600):
        serializer = URLSafeTimedSerializer(self.cf.secret_key)
        try:
            email = serializer.loads(
                token, salt=self.cf.security_salt, max_age=expiration
            )
            return {"email": email, "check": True}
        except SignatureExpired:
            return None
        except BadTimeSignature:
            return None

    def time_now(self) -> datetime:
        return datetime.utcnow()

    def time_then(self) -> datetime:
        return datetime(1980, 1, 1)

    def get_user_string(self, string_length: int = 10) -> str:
        letters = string.ascii_lowercase + "0123456789" + string.ascii_uppercase
        return "".join(random.choice(letters) for _ in range(string_length))

    def _get_indent(self, size: int = 12):
        chars = string.digits
        return "".join(random.choice(chars) for _ in range(size))

    def _get_x_correlation_id(self):
        size = 12
        chars = string.digits
        correlation_id = "".join(random.choice(chars) for _ in range(size)) + "_SC"
        return correlation_id

    def get_indent(self):
        return str(uuid.uuid4())

    def time_delta(self, min: int) -> timedelta:
        return timedelta(minutes=min)

    def hash_password(self, password: str, rounds: int, coding: str) -> str:
        hashed_password = bcrypt.hashpw(
            password.encode(coding), bcrypt.gensalt(rounds=rounds)
        ).decode(coding)
        return hashed_password

    def verify_password(
        self, plain_password: str, hashed_password: str, coding: str
    ) -> bool:
        if bcrypt.checkpw(
            plain_password.encode(coding), hashed_password.encode(coding)
        ):
            return True
        return False

    def random_date(self, start_date, range_in_days):
        days_to_add = np.arange(0, range_in_days)
        rd = np.datetime64(start_date) + np.random.choice(days_to_add)
        return str(rd)

    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        _encode = data.copy()
        if expires_delta:
            _expire = self.time_now() + expires_delta
        else:
            _expire = self.time_now() + self.time_delta(self.cf.token_expire_min)
        _encode.update({"exp": _expire})
        jwt_encode = jwt.encode(
            _encode, self.cf.secret_key, algorithm=self.cf.algorithm
        )
        return jwt_encode
