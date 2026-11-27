from fastapi.testclient import TestClient

from app.models.product import Category, Product


def test_create_product_as_admin(
    client: TestClient,
    admin_headers: dict[str, str],
    sample_category: Category,
):
    payload = {
        "name": "Wireless Mouse",
        "sku": "MS-WIRE-001",
        "price": 49.99,
        "stock_quantity": 25,
        "category_id": sample_category.id,
    }
    response = client.post("/api/v1/products", json=payload, headers=admin_headers)
    assert response.status_code == 201
    body = response.json()
    assert body["data"]["name"] == payload["name"]
    assert body["data"]["sku"] == payload["sku"]


def test_create_product_as_customer_forbidden(
    client: TestClient,
    customer_headers: dict[str, str],
    sample_category: Category,
):
    payload = {
        "name": "Unauthorized Mouse",
        "sku": "MS-UNAUTH-001",
        "price": 20.0,
        "stock_quantity": 5,
        "category_id": sample_category.id,
    }
    response = client.post("/api/v1/products", json=payload, headers=customer_headers)
    assert response.status_code == 403


def test_create_product_unauthenticated(
    client: TestClient,
    sample_category: Category,
):
    payload = {
        "name": "No Auth Mouse",
        "sku": "MS-NOAUTH-001",
        "price": 20.0,
        "stock_quantity": 5,
        "category_id": sample_category.id,
    }
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 401


def test_list_products(client: TestClient, sample_product: Product):
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    body = response.json()
    items = body["data"]["items"]
    assert len(items) >= 1
    assert any(item["id"] == sample_product.id for item in items)
