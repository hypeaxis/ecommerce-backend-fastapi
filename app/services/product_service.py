"""
TUẦN 3 & TUẦN 4: PRODUCT & CATEGORY SERVICE

Nhiệm vụ của tầng Service:
- Xử lý toàn bộ logic nghiệp vụ (kiểm tra tồn tại, validate dữ liệu, điều phối repository).
- Tuyệt đối không import Request hay Response của FastAPI vào đây.

Yêu cầu thực tập sinh tự thực hiện:
- create_category
- create_product (kiểm tra trùng SKU, kiểm tra category tồn tại)
- get_product
- list_products (phân trang và tìm kiếm)
- update_product
- delete_product (xóa mềm)
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.product import Product, Category
from app.schemas.product import ProductCreate, ProductUpdate, CategoryCreate
from app.schemas.common import PageResponse
from app.repositories.product_repository import product_repo, category_repo
from app.core.exceptions import NotFoundException, BadRequestException


class ProductService:
    # TODO: Thực tập sinh tự cài đặt các phương thức nghiệp vụ ở Tuần 3 & 4
    pass


product_service = ProductService()
