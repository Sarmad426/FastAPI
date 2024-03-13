# Create a basic heroes api using official docs

<https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/>

> First setup the project by following this guide. [Click here](../Readme.md)

Add `SQLModel` to the project

```bash
poetry add sqlmodel
```

```python
from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


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
        return {"heroes": heroes}
```

Paste this code in the `main.py` file.

Run the following command

```bash
uvicorn run main:app --reload
```

Open <http://127.0.0.1:8000/heroes/>

You will see empty heroes list in the JSON object.

Open the `database.db` file in **SQLite** browser or any online database tool to add data via sql queries. Otherwise open <http://127.0.0.1:8000/docs#/> and add data via the `post` method.
