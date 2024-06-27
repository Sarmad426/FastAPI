"""
FastAPI todo app Crud Operation API's
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, select, Session
from fastapi.middleware.cors import CORSMiddleware

from typing import Annotated

from database import engine, get_session
from schema import Todo

app = FastAPI()

# Allow middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_db_and_tables():
    """Create database and tables on startup"""
    SQLModel.metadata.create_all(engine)


@app.get("/")
def get_todos(session: Annotated[Session, Depends(get_session)]):
    """
    Returns all the todos
    """
    todos = session.exec(select(Todo)).all()
    return todos


@app.post("/new/todo")
def create_todo(
    session: Annotated[Session, Depends(get_session)], title: str, completed: bool
):
    """
    Creates a new todo

    Parameters
    :title (str)
    :completed (bool)
    """
    todo = Todo(title=title, completed=completed)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.get("/todo/{id}")
def get_todo_by_id(session: Annotated[Session, Depends(get_session)], id: int):
    """
    Return the todo which matches against the id
    """
    todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if not todo:
        return HTTPException(status_code=404, detail=f"Todo not found with id {id}")
    return todo


@app.patch("/edit/todo/{id}")
def edit_todo(
    session: Annotated[Session, Depends(get_session)],
    id: int,
    title: str,
    completed: bool,
):
    """
    Edit and return the todo
    """
    todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if not todo:
        return HTTPException(status_code=404, detail=f"Todo not found with id {id}")
    todo.title = title
    todo.completed = completed
    session.commit()
    return todo


@app.post("/delete/todo")
def delete_todo(session: Annotated[Session, Depends(get_session)], id: int):
    """
    Deletes todo by id
    """
    todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if not todo:
        return HTTPException(status_code=404, detail=f"Todo not found with id {id}")
    session.delete(todo)
    session.commit()
    return todo
