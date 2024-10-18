from poetryclass.practical.testing.main import app, greet

from fastapi.testclient import TestClient


client = TestClient(app)


def test_greet():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello"


def test_greet_name():
    name = "Sarmad"
    response = client.get(f"/{name}")
    assert response.status_code == 200
    assert response.json() == f"Hello {name}"
