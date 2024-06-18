"""
FastAPI Todo app
"""

from fastapi import FastAPI, Depends, Request, HTTPException
from sqlmodel import Session, select
from db_connection import create_db_and_tables, get_session
from schema import Todo

from typing import Annotated

app = FastAPI()

@app.on_event('startup')
def start_events():
    create_db_and_tables()

@app.get('/')
def get_todos(request:Request,session:Annotated[Session,Depends(get_session)]):
    """
    Returns all todos from database
    """
    todos = session.exec(select(Todo)).all()
    if todos:
        return todos
    return "No todos found!"

@app.post('/todos/new-todo')
def new_todo(request:Request,session:Annotated[Session,Depends(get_session)], title:str,completed:bool):
    """
    Creates a new todo
    """
    todo = Todo(title=title,completed=completed)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.get('/todo/{id}')
def get_todo_by_id(request:Request,session:Annotated[Session,Depends(get_session)],id:int) -> Todo:
    """
    Returns a user with provided id
    """
    todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post('/delete/todo/{id}')
def delete_todo_by_id(request:Request,session:Annotated[Session,Depends(get_session)],id:int) -> Todo:
    """
    Deletes a user with provider id
    """
    todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if todo:
        session.remove(todo)
        session.commit()
    raise HTTPException(status_code = 404,detail=f'Todo does not exist with id: {id}')

@app.patch('/edit/todo/{id}')
def update_todo(request:Request,session:Annotated[Session,Depends(get_session)],id:int,title:str,completed) -> Todo:
    """
    Updates the todo with given id
    """
    todo = session.exec(select(Todo).where(Todo.id == id)).first()
    todo.title = title
    todo.completed = completed
