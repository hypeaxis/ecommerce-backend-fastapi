"""
TUẦN 3 & TUẦN 4: PRODUCT & CATEGORY ROUTERS

Yêu cầu:
- POST /categories: Tạo danh mục
- GET /products: Lấy danh sách sản phẩm (có phân trang page, page_size, search, category_id)
- GET /products/{id}: Lấy chi tiết sản phẩm
- POST /products: Tạo sản phẩm mới
- PUT /products/{id}: Sửa sản phẩm
- DELETE /products/{id}: Xóa sản phẩm
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db

router = APIRouter(tags=["Products & Categories"])

# TODO: Thực tập sinh tự cài đặt các endpoints ở Tuần 3 & 4
