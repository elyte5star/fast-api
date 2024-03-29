from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool = True
    message: str = ""
