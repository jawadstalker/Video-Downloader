import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200


def test_download_requires_url_and_format(client):
    response = client.post("/download", data={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "URL and format are required."


def test_batch_requires_list(client):
    response = client.post("/api/batch", json={"urls": "not-a-list"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "URLs must be provided as a list."


def test_invalid_action(client):
    response = client.post("/api/downloads/missing/unknown")
    assert response.status_code == 400
