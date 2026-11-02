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


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="userrole_enum"),
        default=UserRole.CUSTOMER,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
