"""
TUẦN 2: CATEGORY & PRODUCT MODELS

Yêu cầu thực tập sinh tự thực hiện:
1. Bảng categories:
   - id: int (PK)
   - name: str (unique, index)
   - description: text (nullable)
   - relationship: 1 Category có nhiều Products.

2. Bảng products:
   - id: int (PK)
   - name: str (index)
   - sku: str (unique, index) - Mã sản phẩm duy nhất
   - description: text (nullable)
   - price: numeric(10, 2)
   - stock_quantity: int (default 0)
   - is_active: bool (default True)
   - category_id: int (FK -> categories.id)
   - relationship: N-1 với Category, 1-N với OrderItem (ở tuần 6).
"""
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
    )


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")
