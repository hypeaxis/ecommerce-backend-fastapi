"""
TUẦN 6: ORDER REPOSITORY

Yêu cầu thực tập sinh tự thực hiện:
- OrderRepository kế thừa BaseRepository[Order]:
  - get_by_id_with_items(db, id) -> Eager loading order_items để tránh N+1 Query.
  - get_by_user_id(db, user_id)
"""
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.order import Order
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(Order)

    # TODO: Thực tập sinh tự viết các phương thức truy vấn Order ở Tuần 6...
    def get_by_id_with_items(self, db: Session, id: int) -> Optional[Order]:
        """
        Lấy chi tiết đơn hàng kèm toàn bộ danh sách order_items bằng selectinload
        để giải quyết triệt để lỗi N+1 query.
        """
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == id)
        )
        return db.scalar(stmt)

    def get_by_user_id(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        Lấy danh sách đơn hàng của một người dùng kèm items, sắp xếp từ mới nhất đến cũ nhất.
        """
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
            .order_by(Order.id.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())


order_repo = OrderRepository()
