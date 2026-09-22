import pytest
from fastapi.testclient import TestClient
from app.main import app
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
def test_get_turn_returns_focus_and_context(client):
    response = client.get("/api/turn/C1-T011?context=2")
    assert response.status_code == 200
    data = response.json()
    assert data["focus"]["id"] == "C1-T011"
    assert data["focus"]["ts"] == "05:07"
    assert "15 to 20 percent" in data["focus"]["text"]
    ids = [t["id"] for t in data["context"]]
    assert "C1-T011" in ids
    assert len(ids) <= 5
def test_get_turn_unknown_id_returns_404(client):
    response = client.get("/api/turn/C9-T999")
    assert response.status_code == 404
def test_get_turn_default_context_is_two(client):
    response = client.get("/api/turn/C1-T011")
    assert len(response.json()["context"]) == 5
