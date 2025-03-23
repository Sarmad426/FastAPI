# Fast API Response model

Response model is the return type from the path operation. Whereas path operation is an API endpoint.

**POST method:**

```py
# Response model
@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero
```

**GET method:**

```py
@app.get("/heroes/", response_model=list[Hero])
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
```

Docs: <https://sqlmodel.tiangolo.com/tutorial/fastapi/response-model/>
