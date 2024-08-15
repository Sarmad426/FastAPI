"""
Testing FastAPI API endpoints using pytest
"""

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from .main import app, get_session  


def test_create_hero():
        client = TestClient(app)  

        response = client.post(  
            "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
        )
        data = response.json()  

        assert response.status_code == 200  
        assert data["name"] == "Deadpond"  
        assert data["secret_name"] == "Dive Wilson"  
        assert data["age"] is None  
        assert data["id"] is not None  
