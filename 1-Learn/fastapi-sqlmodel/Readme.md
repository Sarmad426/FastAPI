# SQL Model

SQLModel is a library for interacting with SQL databases from Python code, with Python objects. It is designed to be intuitive, easy to use, highly compatible, and robust.

SQLModel is based on Python type annotations, and powered by **Pydantic** and **SQLAlchemy**.

The key features are:

- **Intuitive to write**: Great editor support. Completion everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.
- **Easy to use**: It has sensible defaults and does a lot of work underneath to simplify the code you write.
- **Compatible**: It is designed to be compatible with **FastAPI**, **Pydantic**, and **SQLAlchemy**.
- **Extensible**: You have all the power of **SQLAlchemy** and **Pydantic** underneath.
- **Short**: Minimize code duplication. A single type annotation does a lot of work. No need to duplicate models in **SQLAlchemy** and **Pydantic**.

## Installation

As SQLModel is based on **Pydantic** and **SQLAlchemy**, it requires them. They will be automatically installed when you install **SQLModel**.

```bash
pip install sqlmodel
```

**Tutorial:**

Check out SQLModel official docs tutorial here. <https://sqlmodel.tiangolo.com/tutorial/>

## Fast API SQL model steps from official documentation

```py
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero

@app.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
```

**Run the app:**

```bash
uvicorn main:app --reload
```

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/>
