from typing import Optional


from fastapi import FastAPI, Request, Form
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


sqlite_file_name = "heroes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    name: str = Form(...),
    secret_name: str = Form(...),
    age: int = Form(...),
):
    # Create a new Hero instance
    with Session(engine) as session:
        hero = Hero(name=name, secret_name=secret_name, age=age)

        # Add the hero to the database
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return templates.TemplateResponse(
            "success.html", {"request": request, "name": name}
        )


@app.get("/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return {"heroes": heroes}


@app.get("/heroes/", response_class=HTMLResponse)
async def read_item(request: Request):
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return templates.TemplateResponse(
            request=request, name="index.html", context={"heroes": heroes}
        )
