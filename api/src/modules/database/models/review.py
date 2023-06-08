from modules.database.base import Base
from typing import TYPE_CHECKING
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


if TYPE_CHECKING:
    from .product import Product


class Review(Base):
    rid = Column(String(60), primary_key=True, index=True)
    reviewer_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False, index=True)
    comment = Column(String(600))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    product_id = Column(
        String(60),
        ForeignKey("product.pid", onupdate="CASCADE", ondelete="CASCADE"),
        
        nullable=False,
    )
    product = relationship("Product", back_populates="reviews")
