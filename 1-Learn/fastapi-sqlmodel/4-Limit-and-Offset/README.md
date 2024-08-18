# Limit and Offset

Query parameter will be used here. To learn about them check out the [code here](../../path-query-parameters/main.py)

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
