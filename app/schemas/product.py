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


class CategoryBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None


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
