"""
API Testing
"""

from fastapi import FastAPI

app = FastAPI(title="API testing")


@app.get("/")
def greet():
    """
    Greet message
    """
    return "Hello"


@app.get("/{name}")
def greet_user(name: str):
    """
    Greet msg with name
    """
    return f"Hello {name}"
