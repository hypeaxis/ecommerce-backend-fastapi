"""
TUẦN 5: USER REPOSITORY

Yêu cầu thực tập sinh tự thực hiện:
- UserRepository kế thừa BaseRepository[User]:
  - get_by_email(db, email) -> Optional[User]
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        # TODO: Viết câu lệnh select User theo email ở Tuần 5
        stmt = select(User).where(User.email == email)
        return db.scalar(stmt)


user_repo = UserRepository()
