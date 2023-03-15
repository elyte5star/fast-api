from resources.database.base import Base
from typing import TYPE_CHECKING
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Float,
    ForeignKey,
    Boolean,
    Integer,
)
from datetime import datetime
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Booking(Base):
    oid = Column(String(60), primary_key=True, index=True)
    volume = Column(Integer, nullable=False, index=True)
    sale_price = Column(Float, nullable=False, index=True)
    confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    pid = Column(String(60), ForeignKey("product.pid"))
    owner = relationship("User", back_populates="bookings")
    owner_id = Column(String(60), ForeignKey("user.userid"))
