"""
Testing API's
"""

from poetryclass.practical.testing.main import app

from fastapi.testclient import TestClient


client = TestClient(app)


def test_greet():
    """
    Test the greet API
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello"


def test_greet_name():
    """
    Test the greet_user API
    """
    name = "Sarmad"
    response = client.get(f"/{name}")
    assert response.status_code == 200
    assert response.json() == f"Hello {name}"
