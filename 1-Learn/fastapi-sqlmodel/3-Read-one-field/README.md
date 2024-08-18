# Read one field

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
