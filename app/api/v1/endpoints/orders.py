"""
TUẦN 6: ORDER ROUTERS

Yêu cầu:
- POST /orders: Đặt hàng mới (yêu cầu đăng nhập, transaction)
- GET /orders/my-orders: Lịch sử đơn hàng của tôi
- GET /orders/{order_id}: Chi tiết đơn hàng
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

# TODO: Thực tập sinh tự cài đặt các endpoints đặt hàng ở Tuần 6
