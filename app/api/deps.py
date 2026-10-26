from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Dependency cung cấp session DB và tự động đóng sau khi kết thúc request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: TUẦN 5 - Thực tập sinh bổ sung Dependency get_current_user và require_roles tại đây
