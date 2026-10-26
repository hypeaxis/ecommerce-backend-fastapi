from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Chuẩn hóa wrapper cho toàn bộ response API thành công."""
    success: bool = True
    message: str = "Thành công"
    data: Optional[T] = None


class PageParams(BaseModel):
    """Tham số phân trang từ Query string."""
    page: int = Field(default=1, ge=1, description="Trang hiện tại (bắt đầu từ 1)")
    page_size: int = Field(default=10, ge=1, le=100, description="Số lượng bản ghi mỗi trang (tối đa 100)")
    search: Optional[str] = Field(default=None, description="Từ khóa tìm kiếm")


class PageResponse(BaseModel, Generic[T]):
    """Cấu trúc dữ liệu trả về cho danh sách có phân trang."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)
