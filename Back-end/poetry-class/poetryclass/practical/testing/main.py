"""
API Testing
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def greet():
    """
    Greet message
    """
    return "Hello"


@app.get("/{name}")
def greet(name: str):
    """
    Greet msg with name
    """
    return f"Hello {name}"
