# Multiple models

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
