from resources.database.base import Base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Float,
    ForeignKey,
)
from datetime import datetime
from sqlalchemy.orm import relationship


class Product(Base):
    pid = Column(String(60), primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    image = Column(String(100), nullable=False)
    details = Column(String(500))
    category = Column(String(60), nullable=False, index=True)
    description = Column(String(250), nullable=False)
    price = Column(Float, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    discount = relationship("SpecialDeals")


class SpecialDeals(Base):
    sid = Column(String(60), primary_key=True, index=True)
    new_price = Column(Float, nullable=False, index=True)
    pid = Column(
        String(60), ForeignKey("product.pid"), nullable=False, unique=True
    )
    discount = Column(Float, nullable=False, index=True)
    product = relationship("Product", back_populates="discount")
