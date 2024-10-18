from fastapi import FastAPI
from database import init_db
from auth import router as auth_router

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    init_db()


app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI OAuth2 example with SQLModel"}
