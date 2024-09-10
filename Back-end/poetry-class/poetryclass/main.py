"""
Basic FastAPI api
"""

from fastapi import FastAPI

app = FastAPI(title="Test FastAPI app")


@app.get("/")
def read_root():
    """
    Basic API
    """
    return "Always be progressive"
