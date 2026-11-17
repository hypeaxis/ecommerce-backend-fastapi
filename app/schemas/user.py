"""
TUẦN 5: USER SCHEMAS

Yêu cầu thực tập sinh tự thực hiện:
1. UserRegister: email, password (min 6 ký tự), full_name.
2. UserLogin: email, password.
3. Token: access_token, token_type="bearer", expires_in_minutes.
4. UserResponse: id, email, full_name, role, is_active, created_at.
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from app.models.user import UserRole


# TODO: Thực tập sinh tự hoàn thiện các Schemas User ở Tuần 5

def _normalize_email(v: str) -> str:
    return v.strip().lower()


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=50)
    full_name: str = Field(min_length=2, max_length=100)

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return _normalize_email(str(v))

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        cleaned = v.strip()
        if len(cleaned) < 2:
            raise ValueError(
                "Họ tên không được để trống hoặc chỉ chứa khoảng trắng (tối thiểu 2 ký tự)"
            )
        return cleaned

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Mật khẩu không được chỉ chứa khoảng trắng")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return _normalize_email(str(v))

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
