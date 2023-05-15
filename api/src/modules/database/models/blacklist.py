from modules.database.base import Base
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func


class _BlackList(Base):
    token_id = Column(String(500), primary_key=True, index=True)
    token = Column(String(500), unique=True, index=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
