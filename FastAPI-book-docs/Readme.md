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
