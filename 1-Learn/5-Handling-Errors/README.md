# Handling Errors

## `HTTPException`

Raise an `HTTPException` in your code

`HTTPException` is a normal Python exception with additional data relevant for APIs.

Because it's a Python exception, you don't return it, you raise it.

```py
from fastapi import FastAPI, HTTPException
```

This also means that if you are inside a utility function that you are calling inside of your path operation function, and you `raise` the `HTTPException` from inside of that utility function, it won't run the rest of the code in the path operation function, it will terminate that request right away and send the **HTTP** error from the `HTTPException` to the client.

The benefit of raising an exception over returning a value will be more evident in the section about Dependencies and Security.

In this example, when the client requests an item by an ID that doesn't exist, raise an exception with a status code of 404:

```py
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

### Custom Headers

```py
@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}
```

I have only covered `HTTPException` from the docs. But there is also `RequestValidationError` which is not covered here. And technically it's not essential for all use cases. <https://fastapi.tiangolo.com/tutorial/handling-errors/#override-request-validation-exceptions>

Docs: <https://fastapi.tiangolo.com/tutorial/handling-errors>
