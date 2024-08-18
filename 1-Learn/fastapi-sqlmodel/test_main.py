"""
Testing FastAPI API endpoints using pytest
"""

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from main import app
from db_connection import get_session


TEST_DB_URL = 'sqlite:///testing.db'

def test_create_hero():
    engine = create_engine(  
        TEST_DB_URL, connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  

        def get_session_override():
            return session  

        app.dependency_overrides[get_session] = get_session_override
        

        client = TestClient(app)

        response = client.post(
            "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
        )
        app.dependency_overrides.clear()
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Deadpond"
        assert data["secret_name"] == "Dive Wilson"
        assert data["age"] is None
        assert data["id"] is not None