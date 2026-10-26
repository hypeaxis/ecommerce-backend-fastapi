"""
TUẦN 6: ORDER SCHEMAS

Yêu cầu thực tập sinh tự thực hiện:
1. OrderItemCreate: product_id, quantity.
2. OrderCreate: items (List[OrderItemCreate]).
3. OrderItemResponse: id, product_id, quantity, unit_price.
4. OrderResponse: id, user_id, total_amount, status, created_at, items.
"""
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from app.models.order import OrderStatus


# TODO: Thực tập sinh tự định nghĩa các Schema Order ở Tuần 6
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(min_length=1)
