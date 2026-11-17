from typing import Generator, Optional, Sequence, Union
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.models.user import User, UserRole
from app.repositories.user_repository import user_repo

security_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    """Dependency cung cấp session DB và tự động đóng sau khi kết thúc request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> User:
    """Giải mã Bearer JWT token và trả về thông tin người dùng hiện tại."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedException(
            message="Thông tin xác thực không hợp lệ hoặc bị thiếu"
        )

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject: Optional[str] = payload.get("sub")
        if subject is None:
            raise UnauthorizedException(
                message="Thông tin xác thực không hợp lệ hoặc đã hết hạn"
            )
        user_id = int(subject)
    except (JWTError, ValueError):
        raise UnauthorizedException(
            message="Thông tin xác thực không hợp lệ hoặc đã hết hạn"
        )

    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise UnauthorizedException(message="Người dùng không tồn tại")
    if not user.is_active:
        raise UnauthorizedException(message="Tài khoản đã bị khóa")

    return user


def require_roles(allowed_roles: Sequence[Union[UserRole, str]]):
    """Dependency kiểm tra quyền truy cập dựa trên vai trò (RBAC)."""
    allowed_values = {
        role.value if isinstance(role, UserRole) else str(role)
        for role in allowed_roles
    }

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_role_val = (
            current_user.role.value
            if isinstance(current_user.role, UserRole)
            else str(current_user.role)
        )
        if user_role_val not in allowed_values:
            raise ForbiddenException(
                message="Bạn không có quyền thực hiện hành động này"
            )
        return current_user

    return role_checker
