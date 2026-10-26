"""
TUẦN 6: ORDER & ORDER_ITEM MODELS

Yêu cầu thực tập sinh tự thực hiện:
1. Enum OrderStatus: pending, paid, shipped, cancelled.
2. Bảng orders:
   - id: int (PK)
   - user_id: int (FK -> users.id)
   - total_amount: numeric(12, 2)
   - status: OrderStatus (default pending)
   - relationship: với User và OrderItem.

3. Bảng order_items:
   - id: int (PK)
   - order_id: int (FK -> orders.id)
   - product_id: int (FK -> products.id)
   - quantity: int
   - unit_price: numeric(10, 2)
"""
from enum import Enum
from app.models.base import Base, TimestampMixin


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"

# TODO: Thực tập sinh tự định nghĩa model Order và OrderItem ở Tuần 6
