# Request body

When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.

A request body is data sent by the client to your API. A response body is the data your API sends to the client.

Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time, sometimes they only request a path, maybe with some query parameters, but don't send a body.

To declare request body, you use **Pydantic**.

```py
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```

Docs: <https://fastapi.tiangolo.com/tutorial/body/>

## Cookie parameters

These are pieces of data stored on the client side and sent to the server with every HTTP request. Cookies can be used for session management, personalization, and tracking. They help the server maintain stateful information about the user across multiple requests.

> Cookie parameters can be defined the same way as Path and Query parameters.

```py
from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
```

Docs: <https://fastapi.tiangolo.com/tutorial/cookie-params/>

## Header parameters

These are key-value pairs included in the headers of an HTTP request or response. They provide meta-information about the request or response, such as content type, authentication details, user-agent information, and more. Header parameters are crucial for controlling how the server processes the request and how the client should interpret the response.

```py
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
```

Docs: <https://fastapi.tiangolo.com/tutorial/header-params>
