"""
Auth app backend
"""

from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from db import create_db_and_tables, User, UserCreate, get_session
from sqlmodel import SQLModel, Session, select
from fastapi.middleware.cors import CORSMiddleware
from bcrypt import hashpw, gensalt
import logging
from jose import JWTError, jwt

logging.basicConfig(level=logging.INFO)
loggger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event to create database and tables
    """
    create_db_and_tables()
    yield


class UserLogin(SQLModel):
    """
    User login
    """

    email: str
    password: str


app = FastAPI(lifespan=lifespan)

origins = ["http://127.0.0.1:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """
    Root route
    """
    return {"Hello": "World"}


@app.post("/register/")
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    Creates a user
    """
    loggger.info(f"Creating user {user}")
    hashed_password = hashpw(user.password.encode("utf-8"), gensalt())

    user = User(
        name=user.name,
        email=user.email,
        password=hashed_password.decode("utf-8"),
        role=user.role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"user": user}


@app.post("/login")
async def login(user: UserLogin, session: Session = Depends(get_session)):
    """
    Login function
    """
    loggger.info(f"Logging in user {user}")
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not hashpw(
        user.password.encode("utf-8"), db_user.password.encode("utf-8")
    ) == db_user.password.encode("utf-8"):
        raise HTTPException(status_code=401, detail="Invalid password")

    # create jwt token
    user_data = {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "role": db_user.role,
    }
    token = jwt.encode(user_data, "secret", algorithm="HS256")
    return {"token": token}


@app.get("/secret")
async def secret(token: str):
    """
    Returns the secret token
    """
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/users")
def read_users(session: Annotated[Session, Depends(get_session)]):
    """
    Returns users
    """
    users = session.exec(select(User)).all()
    if users:
        return users
    raise HTTPException(status_code=401, detail="No users found")
