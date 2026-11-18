"""
TUẦN 5: USER SERVICE

Nhiệm vụ:
- register_user: kiểm tra trùng email, băm mật khẩu, tạo user mới.
- authenticate_user: so khớp mật khẩu, sinh JWT token.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.config import settings
from app.models.user import User, UserRole
from app.schemas.user import UserRegister, UserLogin, Token
from app.repositories.user_repository import user_repo
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import BadRequestException, UnauthorizedException


class UserService:
    def register_user(self, db: Session, user_in: UserRegister) -> User:
        normalized_email = user_in.email.strip().lower()
        existing_user = user_repo.get_by_email(db, normalized_email)
        if existing_user:
            raise BadRequestException(
                message="Email đã được sử dụng",
                error_code="EMAIL_ALREADY_EXISTS",
            )

        hashed_password = get_password_hash(user_in.password)
        new_user = User(
            email=normalized_email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            role=UserRole.CUSTOMER,
            is_active=True,
        )
        try:
            db_obj = user_repo.create(db, new_user)
            db.commit()
            return db_obj
        except IntegrityError:
            db.rollback()
            raise BadRequestException(
                message="Email đã được sử dụng",
                error_code="EMAIL_ALREADY_EXISTS",
            )

    def authenticate_user(self, db: Session, login_in: UserLogin) -> Token:
        normalized_email = login_in.email.strip().lower()
        user = user_repo.get_by_email(db, normalized_email)
        if not user or not verify_password(login_in.password, user.hashed_password):
            raise UnauthorizedException(
                message="Email hoặc mật khẩu không chính xác"
            )

        if not user.is_active:
            raise UnauthorizedException(
                message="Tài khoản đã bị khóa hoặc ngừng hoạt động"
            )

        access_token = create_access_token(subject=user.id)
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )


user_service = UserService()
