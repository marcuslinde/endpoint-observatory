from fastapi.testclient import TestClient

from endpoint_observatory.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_endpoint_echoes_id():
    response = client.get("/endpoints/abc")
    assert response.status_code == 200
    assert response.json() == {"endpoint_id": "abc"}
