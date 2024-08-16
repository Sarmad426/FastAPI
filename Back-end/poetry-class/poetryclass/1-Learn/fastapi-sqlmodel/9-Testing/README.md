# Testing FastAPI SQLModel applications

**File Structure:**

```md
-- main.py
-- test_main.py
```

Write all the tests in `test_main.py` file.

**Install required dependencies:**

```bash
python -m pip install requests pytest
```

using poetry:

```bash
poetry add requests pytest
```

## Testing POST request

```py
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

```

Carefully read this part: <https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#testing-database>

We cannot use the same database for testing purposes, it will add a lot of useless stuff. Instead we will override the dependency session.

```py
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from .main import app, get_session  


def test_create_hero():
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

```

Update database name:

```txt
sqlite:///testing.db
```

```py
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from .main import app, get_session  


def test_create_hero():
    engine = create_engine(  
        "sqlite:///testing.db", connect_args={"check_same_thread": False}
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
```

**Run the test:**

```bash
pytest
```

## Configure in-memory database for testing

Sqlite has an in-memory database, which suits perfectly for testing purposes. Which means it won't be create a separate file in the disk.

```py
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool  

from .main import app, get_session


def test_create_hero():
    engine = create_engine(
        "sqlite://",  
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  
    )

```

**Configure pytest:**

```py
import pytest  
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .main import app, get_session


@pytest.fixture(name="session")  
def session_fixture():  
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  


def test_create_hero(session: Session):  
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
```

**Client Fixture:**

Carefully read this part: <https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#client-fixture>

```py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .main import app, get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_session_override():  
        return session

    app.dependency_overrides[get_session] = get_session_override  

    client = TestClient(app)  
    yield client  
    app.dependency_overrides.clear()  


def test_create_hero(client: TestClient):  
    response = client.post(
        "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpond"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] is not None
```

**Add more test:**

```py
# Code above omitted 👆

def test_create_hero(client: TestClient):
    response = client.post(
        "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpond"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] is not None


def test_create_hero_incomplete(client: TestClient):
    # No secret_name
    response = client.post("/heroes/", json={"name": "Deadpond"})
    assert response.status_code == 422


def test_create_hero_invalid(client: TestClient):
    # secret_name has an invalid type
    response = client.post(
        "/heroes/",
        json={
            "name": "Deadpond",
            "secret_name": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert response.status_code == 422

```

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/tests>
