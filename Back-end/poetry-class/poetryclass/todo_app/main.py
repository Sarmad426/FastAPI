"""
FastAPI todo app Crud Operation API's
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, select, Session
from fastapi.middleware.cors import CORSMiddleware

from typing import Annotated

from todo_app import database
from todo_app import schema


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
    SQLModel.metadata.create_all(database.engine)


@app.get("/")
def get_todos(session: Annotated[Session, Depends(database.get_session)]):
    """
    Returns all the todos
    """
    todos = session.exec(select(schema.Todo)).all()
    return todos


@app.post("/new/todo")
def create_todo(
    session: Annotated[Session, Depends(database.get_session)], new_todo: schema.Todo
):
    """
    Creates a new todo

    Parameters
    :title (str)
    :completed (bool)
    """
    todo = schema.Todo(title=new_todo.title, completed=new_todo.completed)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.get("/todo/{id}")
def get_todo_by_id(session: Annotated[Session, Depends(database.get_session)], id: int):
    """
    Return the todo which matches against the id
    """
    todo = session.exec(select(schema.Todo).where(schema.Todo.id == id)).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo not found with id {id}")
    return todo


@app.patch("/edit/todo/{id}")
def edit_todo(
    id: int,
    todo: schema.Todo,
    session: Annotated[Session, Depends(database.get_session)],
):
    """
    Edit and return the todo
    """
    existing_todo = session.exec(
        select(schema.Todo).where(schema.Todo.id == id)
    ).first()
    if not existing_todo:
        raise HTTPException(status_code=404, detail=f"Todo not found with id {id}")

    existing_todo.title = todo.title
    existing_todo.completed = todo.completed
    session.add(existing_todo)
    session.commit()
    session.refresh(existing_todo)

    return existing_todo


@app.delete("/delete/todo/{id}")
def delete_todo(session: Annotated[Session, Depends(database.get_session)], id: int):
    """
    Deletes todo by id
    """
    todo = session.exec(select(schema.Todo).where(schema.Todo.id == id)).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo not found with id {id}")
    session.delete(todo)
    session.commit()
    return todo
