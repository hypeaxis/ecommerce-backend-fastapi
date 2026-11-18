"""
TUẦN 5: AUTHENTICATION ROUTERS

Yêu cầu:
- POST /auth/register: Đăng ký user mới
- POST /auth/login: Đăng nhập lấy access_token (OAuth2 form)
- GET /auth/me: Lấy thông tin user hiện tại qua token
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas import ApiResponse, UserRegister, UserLogin, Token, UserResponse
from app.services.user_service import user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_in: UserRegister,
    db: Session = Depends(get_db),
):
    """Đăng ký tài khoản khách hàng mới."""
    user = user_service.register_user(db, user_in)
    return ApiResponse(
        message="Đăng ký tài khoản thành công",
        data=user,
    )


@router.post(
    "/login",
    response_model=ApiResponse[Token],
    status_code=status.HTTP_200_OK,
)
def login(
    login_in: UserLogin,
    db: Session = Depends(get_db),
):
    """Xác thực người dùng và trả về JWT Access Token."""
    token = user_service.authenticate_user(db, login_in)
    return ApiResponse(
        message="Đăng nhập thành công",
        data=token,
    )


@router.get(
    "/me",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_200_OK,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """Lấy thông tin người dùng hiện tại đang đăng nhập."""
    return ApiResponse(
        message="Lấy thông tin người dùng thành công",
        data=current_user,
    )
