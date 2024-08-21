# Fast API Session dependency

## Dependency

A dependency is specific information that you need at some point. The usual way to get this information is to write code that gets it, right when you need it.

When you’re writing a web service, at some time you may need to do the following:

- Gather input parameters from the HTTP request
- Validate inputs
- Check user authentication and authorization for some endpoints
- Look up data from a data source, often a database
- Emit metrics, logs, or tracking information

## Dependency Injection

Pass any specific information that a function needs into the function. A traditional way to do this is to pass in a helper function, which you then call to get the specific data.

### Dependency Injection in FastAPI

Dependency injection is a design pattern used in FastAPI to manage dependencies between different parts of your application.

Docs: <https://fastapi.tiangolo.com/tutorial/dependencies/#what-is-dependency-injection>

### What is Dependency Injection?

Dependency Injection (DI) is a technique where one object supplies the dependencies of another object. It promotes loose coupling, reusability, and modular design by allowing objects to be easily replaced or modified without affecting other parts of the system.

There are three main types of dependency injection:

- **Constructor Injection**: Dependencies are provided through a class's constructor.
- **Setter Injection**: Dependencies are provided through setter methods.
- **Interface Injection**: Dependencies are provided through an interface.

### Dependency Injection FastAPI

FastAPI uses dependency injection to manage dependencies between various parts of your application, particularly within API endpoints.

Here's how it works in FastAPI:

1. **Declare Dependencies**: Define dependencies as function parameters in your route functions.

2. **Dependency Resolution**: FastAPI resolves dependencies by creating instances of the required classes or functions.

3. **Injection**: Inject instances of dependencies into your route functions automatically.

4. **Automatic Cleanup**: FastAPI handles the lifecycle of dependencies, including cleanup after request processing.

First create a function for getting the database session.

```py
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session
```

For the following docs, the password field wont be there. So remove it from your schema and models.

```py
class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class HeroCreate(HeroBase):
    password: str

class HeroPublic(HeroBase):
    id: int

class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
```

**Using dependency injection:**

```py
# import Depends
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/heroes/", response_model=HeroPublic)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(
    *, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate
):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.delete("/heroes/{hero_id}")
def delete_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
```

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency>
