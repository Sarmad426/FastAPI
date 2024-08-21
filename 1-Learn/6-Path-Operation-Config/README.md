# Path Operation Configuration

There are several parameters that you can pass to your path operation decorator to configure it.

> Notice that these parameters are passed directly to the path operation decorator, not to your path operation function.

## Response Status Code

You can define the (HTTP) `status_code` to be used in the response of your path operation.

You can pass directly the `int` code, like `404`.

But if you don't remember what each number code is for, you can use the shortcut constants in `status`:

```py
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```

## Tags

You can add tags to your path operation, pass the parameter `tags` with a `list` of `str` (commonly just one str):

```py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
```

## Summary and description

```py
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item
```

## Description from docstring

As descriptions tend to be long and cover multiple lines, you can declare the path operation description in the function docstring and FastAPI will read it from there.

You can write Markdown in the docstring, it will be interpreted and displayed correctly (taking into account docstring indentation).

```py
@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
```

### Response description

```py
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
```

**Info:**
> Notice that `response_description` refers specifically to the response, the description refers to the path operation in general.

**Check:**
> OpenAPI specifies that each path operation requires a response description.

So, if you don't provide one, FastAPI will automatically generate one of "Successful response".

### Deprecated path operation

If you want to make a path operation deprecated without removing it, just pass the `deprecated` parameter to `True`.

```py
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
```

Docs: <https://fastapi.tiangolo.com/tutorial/path-operation-configuration>
