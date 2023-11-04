from modules.schemas.responses.base_response import BaseResponse


class TokenResponse(BaseResponse):
    token_data: dict = dict()


