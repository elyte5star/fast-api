from pydantic.typing import Any
from resources.schemas.responses.base_response import BaseResponse


class TokenResponse(BaseResponse):
    token_data: dict = dict()
