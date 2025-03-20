# Response model -  Return type

You can declare the type used for the response by annotating the path operation function return type.

You can use type annotations the same way you would for input data in function parameters, you can use Pydantic models, lists, dictionaries, scalar values like integers, booleans, etc.

```py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
```

It will validate the return type of the data.

**`response_model` parameter:**

If you added the return type annotation, tools and editors would complain with a (correct) error telling you that your function is returning a type (e.g. a dict) that is different from what you declared (e.g. a Pydantic model).

In those cases, you can use the path operation decorator parameter response_model instead of the return type.

```py
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
```

## Response types

Response types (import these classes from `fastapi.responses`) include the following:

- JSONResponse (the default)
- HTMLResponse
- PlainTextResponse
- RedirectResponse
- FileResponse
- StreamingResponse

Docs: <https://fastapi.tiangolo.com/tutorial/response-model>

## Status Code

`HTTP` status code.

```py
from fastapi import FastAPI

app = FastAPI()


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
```

- 100 and above are for "Information". You rarely use them directly. Responses with these status    codes cannot have a body.
- 200 and above are for "Successful" responses. These are the ones you would use the most.
200 is the default status code, which means everything was "OK".
Another example would be 201, "Created". It is commonly used after creating a new record in the database.
- A special case is 204, "No Content". This response is used when there is no content to return to the client, and so the response must not have a body.
- 300 and above are for "Redirection". Responses with these status codes may or may not have a body, except for 304, "Not Modified", which must not have one.
- 400 and above are for "Client error" responses. These are the second type you would probably use the most.
- An example is 404, for a "Not Found" response.
For generic errors from the client, you can just use 400.
- 500 and above are for server errors. You almost never use them directly. When something goes wrong at some part in your application code, or server, it will automatically return one of these status codes.

Read more about **HTTP status codes** <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status>

**Fast Api status codes:**

you can use the convenience variables from `fastapi.status`

```py
from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

They are just a convenience, they hold the same number, but that way you can use the editor's autocomplete to find them.

Docs: <https://fastapi.tiangolo.com/tutorial/response-status-code>
