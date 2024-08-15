# Testing FastAPI SQLModel applications

**File Structure:**

```md
-- main.py
-- test_main.py
```

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

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/tests>
