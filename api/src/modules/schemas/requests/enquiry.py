from pydantic import BaseModel, EmailStr


class Enquiry(BaseModel):
    client_name: str
    client_email: EmailStr
    subject: str
    message: str
