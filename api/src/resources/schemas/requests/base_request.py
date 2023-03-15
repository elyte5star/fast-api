from pydantic import BaseModel, Extra


class RequestBase(BaseModel, extra=Extra.allow):
    pass
