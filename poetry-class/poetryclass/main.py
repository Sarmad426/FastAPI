from typing import Optional


from fastapi import FastAPI, Request, Form
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware


class Todo(SQLModel, table=True):
    """
    Todo Schema (SQLModel)
    - id (int)
    - title (string)
    - completed (boolean)
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    completed: bool = False


sqlite_file_name = "todos.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/todos/", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    title: str = Form(...),
    completed: bool = Form(...),
):
    # Create a new Todo instance
    with Session(engine) as session:
        todo = Todo(title=title, completed=completed)

        # Add the todo to the database
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return templates.TemplateResponse(
            "success.html", {"request": request, "title": title}
        )


@app.get("/")
async def read_todos():
    with Session(engine) as session:
        todos = session.exec(select(Todo)).all()
        return {"todos": todos}


@app.get("/todos")
async def read_item(request: Request):
    with Session(engine) as session:
        todos = session.exec(select(Todo)).all()
        return templates.TemplateResponse(
            request=request, name="index.html", context={"todos": todos}
        )


@app.post("/delete/{todo_id}")
async def delete_todo(todo_id: int):
    """
    Deletes the todo with the specified ID from the database.
    Assumes you have a database session (e.g., SQLAlchemy session) set up.
    """
    with Session(engine) as session:
        # Retrieve the todo by ID
        todo: Todo = session.query(Todo).filter_by(id=todo_id).first()

        if todo:
            # Delete the todo from the database
            session.delete(todo)
            session.commit()
            return {"message": f"Todo with ID {todo_id} deleted successfully"}
        else:
            return {"message": f"Todo with ID {todo_id} not found"}
