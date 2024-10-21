# FastAPI book docs

## URL Path

```py
from fastapi import FastAPI

app = FastAPI()

@app.get("/hi/{who}")
def greet(who):
 return f"Hello? {who}?"
```

## Query Parameters

```py
@app.get("/hi")
def greet(who):
 return f"Hello? {who}?"
```

Query parameter : `http -b localhost:8000/hi?who=Sarmad` = "Helo? Sarmad"

## Body

```py
from fastapi import Body

@app.post("/hi")
def greet(who:str = Body(embed=True)):
 return f"Hello? {who}?"
```

## Header

```py
from fastapi import Header

@app.post("/hi")
def greet(who:str = Header()):
    return f"Hello? {who}?"
```

## Status Code

```py
@app.get("/happy")
def happy(status_code=200):
 return ":)"
```

## Headers

```py
from fastapi import Response
@app.get("/header/{name}/{value}")
def header(name: str, value: str, response:Response):
    response.headers[name]
    return "normal body"
```

## Response types

Response types (import these classes from fastapi.responses) include the following:

- JSONResponse (the default)
- HTMLResponse
- PlainTextResponse
- RedirectResponse
- FileResponse
- StreamingResponse

## Python `async/await`

```python
import asyncio

async def start():
    """
    Start the program
    """
    print("Starting")
    await asyncio.sleep(3)
    print("Terminated. ")

async def running():
    """
    Executing the program
    """
    print("Running: ")

async def main():
    """
    main function
    """
    await asyncio.gather(start(),running())

asyncio.run(main())
```

## Pydantic with FastAPI

```py
from pydantic import BaseModel
from fastapi import FastAPI

# Step 1: Define Pydantic models
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

# Step 2: Create a FastAPI app
app = FastAPI()

# Step 3: Define an API endpoint with Pydantic model
@app.post("/items/")
async def create_item(item: Item):
    # Step 4: Use Pydantic model for request data validation
    return {"name": item.name, "price": item.price, "is_offer": item.is_offer}

# Step 5: Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

## Dependency

A dependency is specific information that you need at some point. The usual way to get this information is to write code that gets it, right when you need it.

When you’re writing a web service, at some time you may need to do the following:

- Gather input parameters from the HTTP request
- Validate inputs
- Check user authentication and authorization for some endpoints
- Look up data from a data source, often a database
- Emit metrics, logs, or tracking information

## Dependency Injection

Pass any specific information that a function needs into the function. A traditional way to do this is to pass in a helper function, which you then call to get the specific data.

### Dependency Injection in FastAPI

Dependency injection is a design pattern used in FastAPI to manage dependencies between different parts of your application.

### What is Dependency Injection?

Dependency Injection (DI) is a technique where one object supplies the dependencies of another object. It promotes loose coupling, reusability, and modular design by allowing objects to be easily replaced or modified without affecting other parts of the system.

There are three main types of dependency injection:

- **Constructor Injection**: Dependencies are provided through a class's constructor.
- **Setter Injection**: Dependencies are provided through setter methods.
- **Interface Injection**: Dependencies are provided through an interface.

### Dependency Injection FastAPI

FastAPI uses dependency injection to manage dependencies between various parts of your application, particularly within API endpoints.

Here's how it works in FastAPI:

1. **Declare Dependencies**: Define dependencies as function parameters in your route functions.

2. **Dependency Resolution**: FastAPI resolves dependencies by creating instances of the required classes or functions.

3. **Injection**: Inject instances of dependencies into your route functions automatically.

4. **Automatic Cleanup**: FastAPI handles the lifecycle of dependencies, including cleanup after request processing.

#### Example

```python
from fastapi import Depends, FastAPI

app = FastAPI()

# Dependency
def get_db():
    db = "fake_db_connection"
    return db

# Route with dependency
@app.get("/items/")
async def read_items(db: str = Depends(get_db)):
    return {"db_connection": db}
```
