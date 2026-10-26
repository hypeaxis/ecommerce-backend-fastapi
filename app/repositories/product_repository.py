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
from sqlalchemy.orm import Session
from app.models.product import Product, Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)

    # TODO: Bổ sung các phương thức truy vấn danh mục nếu cần...


class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)

    # TODO: Thực tập sinh tự cài đặt get_by_sku và search_and_filter ở Tuần 3 & 4...


category_repo = CategoryRepository()
product_repo = ProductRepository()
