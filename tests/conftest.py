from decimal import Decimal
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.deps import get_db
from app.core.security import create_access_token, get_password_hash
from app.models.base import Base
from app.models.product import Category, Product
from app.models.user import User, UserRole

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db: Session) -> User:
    user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("Admin@123"),
        full_name="Admin User",
        role=UserRole.ADMIN,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def customer_user(db: Session) -> User:
    user = User(
        email="customer@example.com",
        hashed_password=get_password_hash("Customer@123"),
        full_name="Customer User",
        role=UserRole.CUSTOMER,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def other_customer_user(db: Session) -> User:
    user = User(
        email="other_customer@example.com",
        hashed_password=get_password_hash("Customer@123"),
        full_name="Other Customer",
        role=UserRole.CUSTOMER,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_token(admin_user: User) -> str:
    return create_access_token(subject=admin_user.id)


@pytest.fixture
def customer_token(customer_user: User) -> str:
    return create_access_token(subject=customer_user.id)


@pytest.fixture
def other_customer_token(other_customer_user: User) -> str:
    return create_access_token(subject=other_customer_user.id)


@pytest.fixture
def admin_headers(admin_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def customer_headers(customer_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {customer_token}"}


@pytest.fixture
def other_customer_headers(other_customer_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {other_customer_token}"}


@pytest.fixture
def sample_category(db: Session) -> Category:
    category = Category(
        name="Electronics",
        description="Electronic devices",
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@pytest.fixture
def sample_product(db: Session, sample_category: Category) -> Product:
    product = Product(
        name="Mechanical Keyboard",
        sku="KB-MECH-001",
        price=Decimal("100.00"),
        stock_quantity=10,
        category_id=sample_category.id,
        is_active=True,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
