from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Kiểm tra endpoint /healthz hoạt động chuẩn 200 OK."""
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
