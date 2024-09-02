# Testing

## Using `TestClient`

**Info:**

To use `TestClient` you need to install `httpx`.

Make sure virtualenv is activated.

```py
pip install httpx
```

Import `TestClient`.

Create a `TestClient` by passing your FastAPI application to it.

Create functions with a name that starts with `test_` (this is standard `pytest` conventions).

Use the `TestClient` object the same way as you do with `httpx`.

Write simple `assert` statements with the standard Python expressions that you need to check (again, standard `pytest`).

```py
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

**Tip:**

Notice that the testing functions are normal `def`, not `async def`.

And the calls to the client are also normal calls, not using `await`.

This allows you to use `pytest` directly without complications.

### Separating tests

File structure:

```txt
.
├── app
│   ├── __init__.py
│   └── main.py
```

Im `main.py` we have the following code.

```py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
```

**Testing file:**

```py
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Code in it.

```py
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

**Install `pytest`**

```bash
pip install pytest
```

**Run tests:**

```bash
pytest
```

Docs: <https://fastapi.tiangolo.com/tutorial/testing/>
