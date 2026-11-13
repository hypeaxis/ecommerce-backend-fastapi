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
from sqlalchemy import select, func
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
    # Tuần 4: Tìm kiếm, lọc theo danh mục và phân trang
    def search_and_filter(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 10,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Product], int]:
        stmt = select(Product).where(Product.is_active.is_(True))
        count_stmt = select(func.count()).select_from(Product).where(Product.is_active.is_(True))

        if category_id is not None:
            stmt = stmt.where(Product.category_id == category_id)
            count_stmt = count_stmt.where(Product.category_id == category_id)

        if search and search.strip():
            escaped_search = (
                search.strip()
                .replace("\\", "\\\\")
                .replace("%", "\\%")
                .replace("_", "\\_")
            )
            search_pattern = f"%{escaped_search}%"
            stmt = stmt.where(Product.name.ilike(search_pattern, escape="\\"))
            count_stmt = count_stmt.where(Product.name.ilike(search_pattern, escape="\\"))

        total = db.scalar(count_stmt) or 0
        stmt = (
            stmt.options(joinedload(Product.category))
            .order_by(Product.id.desc())
            .offset(skip)
            .limit(limit)
        )
        items = list(db.scalars(stmt).all())

        return items, total

category_repo = CategoryRepository()
product_repo = ProductRepository()
