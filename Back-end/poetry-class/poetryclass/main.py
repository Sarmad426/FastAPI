from fastapi import FastAPI

app = FastAPI(title="Test FastAPI app")


@app.get("/")
def read_root():
    return "Always be progressive"
