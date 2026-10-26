"""
TUẦN 6: ORDER REPOSITORY

Yêu cầu thực tập sinh tự thực hiện:
- OrderRepository kế thừa BaseRepository[Order]:
  - get_by_id_with_items(db, id) -> Eager loading order_items để tránh N+1 Query.
  - get_by_user_id(db, user_id)
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.order import Order
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(Order)

    # TODO: Thực tập sinh tự viết các phương thức truy vấn Order ở Tuần 6...


order_repo = OrderRepository()
