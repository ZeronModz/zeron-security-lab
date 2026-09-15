import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Zeron Web Security Testing Suite"
    assert "version" in data


async def test_health(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


async def test_system_info(client):
    response = await client.get("/api/v1/system/info")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "python_version" in data["data"]


async def test_system_capabilities(client):
    response = await client.get("/api/v1/system/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "GET" in data["data"]["supported_methods"]


async def test_web_fetch_empty_url(client):
    response = await client.post("/api/v1/web/fetch", json={"url": ""})
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "INVALID_URL"


async def test_web_fetch_invalid_scheme(client):
    response = await client.post("/api/v1/web/fetch", json={"url": "ftp://example.com"})
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "INVALID_SCHEME"


async def test_web_fetch_private_ip(client):
    response = await client.post("/api/v1/web/fetch", json={"url": "http://127.0.0.1/admin"})
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "PRIVATE_TARGET"


async def test_web_fetch_localhost(client):
    response = await client.post("/api/v1/web/fetch", json={"url": "http://localhost:8080"})
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "PRIVATE_TARGET"


async def test_web_fetch_private_network_10(client):
    response = await client.post("/api/v1/web/fetch", json={"url": "http://10.0.0.1/secret"})
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "PRIVATE_TARGET"


async def test_web_fetch_private_network_192(client):
    response = await client.post("/api/v1/web/fetch", json={"url": "http://192.168.1.1/"})
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "PRIVATE_TARGET"


async def test_api_request_invalid_url(client):
    response = await client.post("/api/v1/api/request", json={"url": "not-a-url"})
    data = response.json()
    assert data["success"] is False


async def test_api_request_private_ip(client):
    response = await client.post("/api/v1/api/request", json={"url": "http://127.0.0.1/api"})
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "PRIVATE_TARGET"


async def test_cloudflare_health(client):
    response = await client.get("/api/v1/cloudflare/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


async def test_recaptcha_health(client):
    response = await client.get("/api/v1/recaptcha/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


async def test_targets_crud(client):
    create_resp = await client.post("/api/v1/targets", json={
        "url": "https://example.com",
        "name": "Test Target",
        "is_authorized": True,
    })
    assert create_resp.status_code == 200
    data = create_resp.json()
    assert data["success"] is True
    target_id = data["data"]["id"]

    list_resp = await client.get("/api/v1/targets")
    assert list_resp.status_code == 200
    list_data = list_resp.json()
    assert list_data["data"]["total"] >= 1

    del_resp = await client.delete(f"/api/v1/targets/{target_id}")
    assert del_resp.status_code == 200
    del_data = del_resp.json()
    assert del_data["success"] is True


async def test_history(client):
    response = await client.get("/api/v1/history")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


async def test_security_headers(client):
    response = await client.get("/")
    assert "X-Content-Type-Options" in response.headers
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "X-Frame-Options" in response.headers
    assert response.headers["X-Frame-Options"] == "DENY"


async def test_request_id_header(client):
    response = await client.get("/api/v1/health")
    assert "X-Request-ID" in response.headers
