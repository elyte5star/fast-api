from modules.database.base import Base
from typing import TYPE_CHECKING
from sqlalchemy.ext.mutable import MutableList

from sqlalchemy import (
    Column,
    String,
    DateTime,
    PickleType,
    ForeignKey,
    Float
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .user import _User  # noqa: F401


class _Booking(Base):
    oid = Column(String(60), primary_key=True, index=True)
    cart = Column(MutableList.as_mutable(PickleType), default=[])
    total_price = Column(Float, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship("_User", back_populates="bookings")
    owner_id = Column(String(60), ForeignKey("_user.userid", ondelete="CASCADE"))
