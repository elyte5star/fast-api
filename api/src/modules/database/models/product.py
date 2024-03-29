from modules.database.base import Base
from typing import TYPE_CHECKING
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Float,
    ForeignKey,
    Integer
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .review import Review


class Product(Base):
    pid = Column(String(60), primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    image = Column(String(100), nullable=False)
    details = Column(String(500))
    category = Column(String(60), nullable=False, index=True)
    description = Column(String(250), nullable=False)
    price = Column(Float, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    stock_quantity = Column(Integer, nullable=False, index=True)
    discount = relationship("SpecialDeals", back_populates="product",cascade='save-update, merge, delete',
        passive_deletes=True,)
    reviews = relationship("Review", back_populates="product",cascade='save-update, merge, delete',passive_deletes=True)


class SpecialDeals(Base):
    sid = Column(String(60), primary_key=True, index=True)
    new_price = Column(Float, nullable=False, index=True)
    product_id = Column(String(60), ForeignKey("product.pid",ondelete='CASCADE'), unique=True,nullable=False)
    discount = Column(Float, nullable=False, index=True)
    product = relationship("Product", back_populates="discount")
