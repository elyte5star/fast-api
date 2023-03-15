from resources.database.base import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .booking import Booking  # noqa: F401


class User(Base):
    userid = Column(String(40), primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    discount = Column(Float)
    telephone = Column(Integer, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    bookings = relationship("Booking", back_populates="owner")
