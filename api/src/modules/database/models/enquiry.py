from modules.database.base import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func


class _Enquiry(Base):
    eid = Column(String(60), primary_key=True, index=True)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(60), nullable=False)
    country = Column(String(60), nullable=False)
    subject = Column(String(100), index=True)
    message = Column(String(600))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
