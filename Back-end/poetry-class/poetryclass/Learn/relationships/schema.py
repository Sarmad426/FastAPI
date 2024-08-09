from sqlmodel import SQLModel, Field, Relationship


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamPublic(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: int | None = None


class HeroPublic(SQLModel):
    id: int
    name: str
    secret_name: str
    age: int | None = None


class HeroPublicWithTeam(HeroPublic):
    team: TeamPublic | None = None


class TeamPublicWithHeroes(TeamPublic):
    heroes: list[HeroPublic] = []
