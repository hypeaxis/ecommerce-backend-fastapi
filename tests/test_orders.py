from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.product import Category, Product


def test_create_order_success_deducts_stock(
    client: TestClient,
    db: Session,
    customer_headers: dict[str, str],
    sample_product: Product,
):
    payload = {
        "items": [
            {"product_id": sample_product.id, "quantity": 3},
        ]
    }
    response = client.post("/api/v1/orders", json=payload, headers=customer_headers)
    assert response.status_code == 201
    body = response.json()
    assert Decimal(str(body["data"]["total_amount"])) == Decimal("300.00")

    db.refresh(sample_product)
    assert sample_product.stock_quantity == 7


def test_create_order_insufficient_stock_rollback(
    client: TestClient,
    db: Session,
    customer_headers: dict[str, str],
    sample_category: Category,
    sample_product: Product,
):
    out_of_stock_product = Product(
        name="Limited GPU",
        sku="GPU-LIM-001",
        price=Decimal("500.00"),
        stock_quantity=1,
        category_id=sample_category.id,
        is_active=True,
    )
    db.add(out_of_stock_product)
    db.commit()
    db.refresh(out_of_stock_product)

    payload = {
        "items": [
            {"product_id": sample_product.id, "quantity": 2},
            {"product_id": out_of_stock_product.id, "quantity": 5},
        ]
    }
    response = client.post("/api/v1/orders", json=payload, headers=customer_headers)
    assert response.status_code == 400
    assert response.json()["error_code"] == "INSUFFICIENT_STOCK"

    db.refresh(sample_product)
    assert sample_product.stock_quantity == 10, (
        "Lỗi rollback: Tồn kho của sản phẩm hợp lệ đã bị trừ sai!"
    )
    assert db.scalars(select(Order)).all() == []


def test_get_order_detail_owner_and_admin(
    client: TestClient,
    customer_headers: dict[str, str],
    admin_headers: dict[str, str],
    sample_product: Product,
):
    create_resp = client.post(
        "/api/v1/orders",
        json={"items": [{"product_id": sample_product.id, "quantity": 1}]},
        headers=customer_headers,
    )
    assert create_resp.status_code == 201
    order_id = create_resp.json()["data"]["id"]

    owner_resp = client.get(f"/api/v1/orders/{order_id}", headers=customer_headers)
    assert owner_resp.status_code == 200

    admin_resp = client.get(f"/api/v1/orders/{order_id}", headers=admin_headers)
    assert admin_resp.status_code == 200


def test_get_order_detail_other_customer_forbidden(
    client: TestClient,
    customer_headers: dict[str, str],
    other_customer_headers: dict[str, str],
    sample_product: Product,
):
    create_resp = client.post(
        "/api/v1/orders",
        json={"items": [{"product_id": sample_product.id, "quantity": 1}]},
        headers=customer_headers,
    )
    assert create_resp.status_code == 201
    order_id = create_resp.json()["data"]["id"]

    other_resp = client.get(f"/api/v1/orders/{order_id}", headers=other_customer_headers)
    assert other_resp.status_code == 403
