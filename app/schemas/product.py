"""
TUẦN 3 & TUẦN 4: PRODUCT & CATEGORY SCHEMAS

Yêu cầu thực tập sinh tự thực hiện:
1. CategoryCreate, CategoryResponse
2. ProductCreate (có validation giá > 0, tên không rỗng, sku in hoa)
3. ProductUpdate (các trường tùy chọn)
4. ProductResponse (from_attributes=True)
"""
from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, ConfigDict

def _validate_non_blank_name(v: str, field_label: str = "Tên sản phẩm") -> str:
    cleaned = v.strip()
    if len(cleaned) < 2:
        raise ValueError(
            f"{field_label} không được để trống hoặc chỉ chứa khoảng trắng (tối thiểu 2 ký tự)"
        )
    return cleaned


def _validate_and_normalize_sku(v: str) -> str:
    cleaned = v.strip().upper()
    if len(cleaned) < 3:
        raise ValueError(
            "Mã SKU không được để trống hoặc chỉ chứa khoảng trắng (tối thiểu 3 ký tự)"
        )
    return cleaned

class CategoryBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None

    # Tuần 4: Chuẩn hóa và chặn tên danh mục chỉ chứa khoảng trắng
    @field_validator("name")
    @classmethod
    def validate_category_name(cls, v: str) -> str:
        return _validate_non_blank_name(v, field_label="Tên danh mục")


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# TODO: Thực tập sinh hoàn thiện ProductCreate, ProductUpdate, ProductResponse ở Tuần 3 & 4
class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    sku: str = Field(min_length=3, max_length=50)
    description: Optional[str] = None
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    category_id: int

    # Tuần 4: Chuẩn hóa và chặn tên sản phẩm chỉ chứa khoảng trắng
    @field_validator("name")
    @classmethod
    def validate_product_name(cls, v: str) -> str:
        return _validate_non_blank_name(v, field_label="Tên sản phẩm")

    # Tuần 4: Cắt khoảng trắng và chuẩn hóa mã kho SKU thành chữ in hoa
    @field_validator("sku")
    @classmethod
    def validate_product_sku(cls, v: str) -> str:
        return _validate_and_normalize_sku(v)


class ProductCreate(ProductBase):
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = True


class ProductResponse(ProductBase):
    id: int
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=200)
    sku: Optional[str] = Field(default=None, min_length=3, max_length=50)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None
    category_id: Optional[int] = None

    # Tuần 4: Validate name và sku khi cập nhật sản phẩm (nếu có truyền lên)
    @field_validator("name")
    @classmethod
    def validate_product_name(cls, v: Optional[str]) -> Optional[str]:
        return _validate_non_blank_name(v, field_label="Tên sản phẩm") if v is not None else v

    @field_validator("sku")
    @classmethod
    def validate_product_sku(cls, v: Optional[str]) -> Optional[str]:
        return _validate_and_normalize_sku(v) if v is not None else v