"""
TUẦN 3 & TUẦN 4: PRODUCT & CATEGORY REPOSITORIES

Yêu cầu thực tập sinh tự thực hiện:
1. CategoryRepository kế thừa BaseRepository[Category]:
   - get_by_name(db, name)
2. ProductRepository kế thừa BaseRepository[Product]:
   - get_by_sku(db, sku)
   - get_by_id_with_category(db, id)
   - search_and_filter(db, skip, limit, category_id, search) -> (items, total)
"""
from typing import Optional, List, Tuple
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.models.product import Product, Category
from app.repositories.base import BaseRepository

class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)

    # TODO: Bổ sung các phương thức truy vấn danh mục nếu cần...
    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        stmt = select(Category).where(Category.name == name)
        return db.scalar(stmt)

class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)

    # Tuần 3
    def get_by_sku(self, db: Session, sku: str) -> Optional[Product]:
        stmt = select(Product).where(Product.sku == sku)
        return db.scalar(stmt)

    def get_by_id_with_category(self, db: Session, id: int) -> Optional[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.id == id)
        )
        return db.scalar(stmt)

    def get_multi_active(self, db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.is_active.is_(True))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())
    # TODO: Thực tập sinh tự cài đặt get_by_sku và search_and_filter ở Tuần 3 & 4...


category_repo = CategoryRepository()
product_repo = ProductRepository()
