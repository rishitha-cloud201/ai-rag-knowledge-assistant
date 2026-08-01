from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "AI RAG Knowledge Assistant"


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_question_validation() -> None:
    response = client.post(
        "/api/v1/questions/ask",
        json={"question": "a"},
    )

    assert response.status_code == 422