# Models with relationships

Carefully Read these parts:

- <https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#dont-include-all-the-data>
- <https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#what-data-to-include>

Add these models.

```py
class HeroPublicWithTeam(HeroPublic):
    team: TeamPublic | None = None

class TeamPublicWithHeroes(TeamPublic):
    heroes: list[HeroPublic] = []
```

Update the get operations

```py

@app.get("/heroes/{hero_id}", response_model=HeroPublicWithTeam)
def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.get("/teams/{team_id}", response_model=TeamPublicWithHeroes)
def read_team(*, team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

```

Docs : <https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/>
