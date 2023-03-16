from modules.database.base import Base
from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime


class BlackList(Base):
    token_id = Column(String(500), primary_key=True, index=True)
    token = Column(String(500), unique=True, index=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
