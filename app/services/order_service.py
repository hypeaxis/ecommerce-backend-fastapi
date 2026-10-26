"""
TUẦN 6: ORDER SERVICE (DATABASE TRANSACTION & ACID)

Nhiệm vụ trọng tâm:
- create_order: bọc trong 1 Transaction duy nhất!
  1. Kiểm tra tồn kho của từng sản phẩm.
  2. Trừ stock_quantity của sản phẩm.
  3. Tính tổng tiền dựa trên giá trong DB (không tin giá client gửi).
  4. Lưu order và order_items.
  5. Nếu bất kỳ sản phẩm nào thiếu hàng -> rollback toàn bộ!
"""
from typing import List
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderCreate
from app.repositories.order_repository import order_repo
from app.repositories.product_repository import product_repo
from app.core.exceptions import BadRequestException, NotFoundException


class OrderService:
    # TODO: Thực tập sinh tự cài đặt nghiệp vụ đặt hàng và transaction ở Tuần 6
    pass


order_service = OrderService()
