# Fast API SQL model code examples from official documentation

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

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/>

**Run the app:**

```bash
uvicorn main:app --reload
```

## Response model

```py
# Response model
@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero

@app.get("/heroes/", response_model=list[Hero])
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
```

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/response-model/>

## Multiple models

```py
# For creating a new Hero because id is not required from the post method
class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: int | None = None

# Returning a todo because id is required from the get method
class HeroPublic(SQLModel):
    id: int
    name: str
    secret_name: str
    age: int | None = None
```

**Updated the post method:**

```py
@app.post("/heroes/", response_model=HeroPublic) # Return type is `HeroPublic`
def create_hero(hero: HeroCreate): # using the HeroCreate method
    with Session(engine) as session:
        db_hero = Hero.model_validate(hero) # validating the hero
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero
```

**Terminate redundancy using Inheritance:**

Creating a parent to inherit fields from

```py
class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
```

Inherit the Hero model

```py
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
```

Inherit other models

```py
class HeroCreate(HeroBase):
    pass

class HeroPublic(HeroBase):
    id: int
```

With that it won't ask for id field in the interactive docs of Swagger UI. <http://127.0.0.1:8000/docs>

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models>

## Read one field

```py
from fastapi import HTTPException

@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero: # validating
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero
```

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/read-one/>

## Limit and Offset

Query parameter will be used here. To learn about them check out the [code here](../path-query-parameters/main.py)

```py
from fastapi import FastAPI, HTTPException, Query

@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(offset: int = 0, limit: int = Query(default=100, le=100)):
    with Session(engine) as session:
        heroes = session.exec(select(Hero).offset(offset).limit(limit)).all() # limit & offset
        return heroes
```

It has to be less than or equal to 100 with le=100.

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/limit-and-offset/>

## Updating data

Let's add a new field `hashed_password` to the `Hero` model.

```py
class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()


class HeroCreate(HeroBase):
    password: str


class HeroPublic(HeroBase):
    id: int


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    password: str | None = None
```

**Patch method:**

```py
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate):
    with Session(engine) as session:
        db_hero = session.get(Hero, hero_id)
        if not db_hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        hero_data = hero.model_dump(exclude_unset=True)
        db_hero.sqlmodel_update(hero_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero
```

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/update>

## Updating with Extra Data (Hashed Passwords)

Fake password hashing while creating new hero

SQLModel models have a parameter `update` in Hero.model_validate() that takes a dictionary with extra data, or data that should take precedence.

```py
def hash_password(password: str) -> str:
    # Use something like passlib here
    return f"not really hashed {password} hehehe"

@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate):
    hashed_password = hash_password(hero.password)
    with Session(engine) as session:
        extra_data = {"hashed_password": hashed_password}
        db_hero = Hero.model_validate(hero, update=extra_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero    
```

**Update the already existing data:**

```py
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate):
    with Session(engine) as session:
        db_hero = session.get(Hero, hero_id)
        if not db_hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        hero_data = hero.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in hero_data:
            password = hero_data["password"]
            hashed_password = hash_password(password)
            extra_data["hashed_password"] = hashed_password
        db_hero.sqlmodel_update(hero_data, update=extra_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero
```

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/update-extra-data>

## Delete data

```py
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}
```

Docs:<https://sqlmodel.tiangolo.com/tutorial/fastapi/delete/>
