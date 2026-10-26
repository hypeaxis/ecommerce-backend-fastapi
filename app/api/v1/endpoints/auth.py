"""
TUẦN 5: AUTHENTICATION ROUTERS

Yêu cầu:
- POST /auth/register: Đăng ký user mới
- POST /auth/login: Đăng nhập lấy access_token (OAuth2 form)
- GET /auth/me: Lấy thông tin user hiện tại qua token
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

# TODO: Thực tập sinh tự cài đặt các endpoints xác thực ở Tuần 5
