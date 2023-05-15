from modules.database.base import Base
from sqlalchemy import Boolean, Column,String, DateTime, Float
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from .booking import _Booking  # noqa: F401


class _User(Base):
    userid = Column(String(40), primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    discount = Column(Float)
    telephone = Column(String(20), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    bookings = relationship("_Booking", back_populates="owner",cascade='save-update, merge, delete',passive_deletes=True)
