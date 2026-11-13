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
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import (
    ApiResponse,
    PageResponse,
    CategoryCreate,
    CategoryResponse,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

from app.services.product_service import product_service
router = APIRouter(tags=["Products & Categories"])

# TODO: Thực tập sinh tự cài đặt các endpoints ở Tuần 3 & 4
# Tuần 3

# Endpoint cho các danh mục
@router.post(
    "/categories",
    response_model=ApiResponse[CategoryResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db),
):
    """Tạo danh mục sản phẩm mới."""
    category = product_service.create_category(db, category_in)
    return ApiResponse(
        message="Tạo danh mục thành công",
        data=category,
    )

@router.get(
    "/categories",
    response_model=ApiResponse[list[CategoryResponse]],
    status_code=status.HTTP_200_OK,
)
def get_categories(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Lấy danh sách các danh mục sản phẩm."""
    categories = product_service.get_categories(db, skip=skip, limit=limit)
    return ApiResponse(
        message="Lấy danh sách danh mục thành công",
        data=categories,
    )

#Endpoints CRUD cho Sản phẩm(Product)

@router.post(
    "/products",
    response_model=ApiResponse[ProductResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
):
    """Tạo sản phẩm mới."""
    product = product_service.create_product(db, product_in)
    return ApiResponse(
        message="Tạo sản phẩm thành công",
        data=product,
    )

# Tuần 4: Nâng cấp endpoint GET /products hỗ trợ phân trang, tìm kiếm và lọc
@router.get(
    "/products",
    response_model=ApiResponse[PageResponse[ProductResponse]],
    status_code=status.HTTP_200_OK,
)
def get_products(
    page: int = Query(default=1, ge=1, description="Trang hiện tại (bắt đầu từ 1)"),
    page_size: int = Query(default=10, ge=1, le=100, description="Số lượng bản ghi mỗi trang (tối đa 100)"),
    category_id: Optional[int] = Query(default=None, description="Lọc theo ID danh mục"),
    search: Optional[str] = Query(default=None, description="Tìm kiếm tương đối theo tên sản phẩm"),
    db: Session = Depends(get_db),
):
    """Lấy danh sách sản phẩm hỗ trợ phân trang, tìm kiếm và lọc theo danh mục."""
    result = product_service.list_products(
        db=db,
        page=page,
        page_size=page_size,
        category_id=category_id,
        search=search,
    )
    return ApiResponse(
        message="Lấy danh sách sản phẩm thành công",
        data=result,
    )

@router.get(
    "/products/{id}",
    response_model=ApiResponse[ProductResponse],
    status_code=status.HTTP_200_OK,
)
def get_product(
    id: int,
    db: Session = Depends(get_db),
):
    """Lấy thông tin chi tiết một sản phẩm theo ID."""
    product = product_service.get_product(db, id)
    return ApiResponse(
        message="Lấy thông tin sản phẩm thành công",
        data=product,
    )

@router.put(
    "/products/{id}",
    response_model=ApiResponse[ProductResponse],
    status_code=status.HTTP_200_OK,
)
def update_product(
    id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
):
    """Cập nhật thông tin sản phẩm theo ID."""
    product = product_service.update_product(db, id, product_in)
    return ApiResponse(
        message="Cập nhật sản phẩm thành công",
        data=product,
    )

@router.delete(
    "/products/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
):
    """Xóa mềm sản phẩm theo ID."""
    product_service.delete_product(db, id)
    return None