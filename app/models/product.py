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
from typing import Optional
from sqlalchemy import String, Numeric, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


# TODO: Thực tập sinh hoàn thiện Category model ở Tuần 2
class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


# TODO: Thực tập sinh hoàn thiện Product model ở Tuần 2
class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    # TODO: Thêm sku, price, stock_quantity, category_id và relationship...
