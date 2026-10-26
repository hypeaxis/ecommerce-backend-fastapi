"""
TUẦN 5: USER SERVICE

Nhiệm vụ:
- register_user: kiểm tra trùng email, băm mật khẩu, tạo user mới.
- authenticate_user: so khớp mật khẩu, sinh JWT token.
"""
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserRegister, UserLogin, Token
from app.repositories.user_repository import user_repo
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import BadRequestException, UnauthorizedException


class UserService:
    # TODO: Thực tập sinh tự cài đặt logic đăng ký và đăng nhập ở Tuần 5
    pass


user_service = UserService()
