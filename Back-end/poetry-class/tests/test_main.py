import pytest
from fastapi.testclient import TestClient
from poetryclass.todo_app.main import app, get_session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

# Create a new database session for testing
DATABASE_URL = "sqlite://"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

# Dependency override to use the test database
def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

@pytest.fixture(name="client")
def client_fixture():
    SQLModel.metadata.create_all(engine)
    with TestClient(app) as client:
        yield client
    SQLModel.metadata.drop_all(engine)

def test_get_todos(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo(client):
    response = client.post("/new/todo", json={"title": "Test Todo", "completed": False})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["completed"] is False
    assert "id" in data

def test_get_todo_by_id(client):
    response = client.post("/new/todo", json={"title": "Test Todo", "completed": False})
    todo_id = response.json()["id"]
    response = client.get(f"/todo/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["completed"] is False

def test_edit_todo(client):
    response = client.post("/new/todo", json={"title": "Test Todo", "completed": False})
    todo_id = response.json()["id"]
    response = client.patch(f"/edit/todo/{todo_id}", json={"title": "Updated Todo", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Todo"
    assert data["completed"] is True

def test_delete_todo(client):
    response = client.post("/new/todo", json={"title": "Test Todo", "completed": False})
    todo_id = response.json()["id"]
    response = client.delete(f"/delete/todo/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["completed"] is False
    response = client.get(f"/todo/{todo_id}")
    assert response.status_code == 404
