"""
TUẦN 6: ORDER SCHEMAS

Yêu cầu thực tập sinh tự thực hiện:
1. OrderItemCreate: product_id, quantity.
2. OrderCreate: items (List[OrderItemCreate]).
3. OrderItemResponse: id, product_id, quantity, unit_price.
4. OrderResponse: id, user_id, total_amount, status, created_at, items.
"""
from datetime import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field, ConfigDict, field_validator
from app.models.order import OrderStatus


# TODO: Thực tập sinh tự định nghĩa các Schema Order ở Tuần 6
class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="ID của sản phẩm cần đặt")
    quantity: int = Field(..., gt=0, description="Số lượng đặt mua phải lớn hơn 0")


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(..., min_length=1, description="Đơn hàng phải có ít nhất 1 sản phẩm")

    @field_validator("items")
    @classmethod
    def validate_unique_products(cls, items: List[OrderItemCreate]) -> List[OrderItemCreate]:
        product_ids = [item.product_id for item in items]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("Các sản phẩm trong đơn hàng không được trùng lặp")
        return items


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemResponse] = []
