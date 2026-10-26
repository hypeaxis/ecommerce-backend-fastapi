"""
TUẦN 2 & TUẦN 5: USER MODEL

Yêu cầu thực tập sinh tự thực hiện:
1. Định nghĩa Enum UserRole (admin, customer).
2. Tạo model User kế thừa từ Base và TimestampMixin.
3. Các trường cần có:
   - id: int (Primary key, autoincrement)
   - email: str (unique, index, nullable=False)
   - hashed_password: str (nullable=False)
   - full_name: str (nullable=False)
   - role: UserRole (default là customer)
   - is_active: bool (default là True)
   - Relationship với Order (nếu có ở tuần 6).
"""
from enum import Enum
from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin


class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


# TODO: Thực tập sinh hoàn thiện class User theo yêu cầu Tuần 2
class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    # TODO: Thêm hashed_password, full_name, role, is_active tại đây...
