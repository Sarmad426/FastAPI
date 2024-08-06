"""
FastAPI todo app Crud Operation API's
"""

from typing import Annotated, Union

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import SQLModel, select, Session


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


@app.get('/', response_model=list[Todo])
def read_todos(session: Session = Depends(get_session)) -> Union[list[Todo], JSONResponse]:
    """
    Read all todos from database

    Args:
        session (Session): Database session

    Returns:
        Union[List[Todo], JSONResponse]: List of Todos or error message
    """
    try:
        query = select(Todo)
        todos: list[Todo] = session.exec(query).all()
        if not todos:
            return JSONResponse(status_code=404, content={"error": {"code": 404, "message": "No todos in the database"}})
        return todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/new/todo')
def create_new_todo(session:Annotated[Session,Depends(get_session)],todo:Todo) -> Todo:
    """Create new todo

    Args:
        todo (Todo)
    """
    new_todo = Todo(title=todo.title,completed=todo.completed)
    session.add(new_todo)
    try:
        session.commit()
        session.refresh(new_todo)
    except Exception as e:
        # Undo partial changes if error happens
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return new_todo


@app.get("/todo/{id}")
def get_todo_by_id(session: Annotated[Session, Depends(get_session)], id: int):
    """
    Return the todo which matches against the id
    """
    try:
        query = select(Todo).where(Todo.id == id)
        todo: Todo | None = session.exec(query).first()
        if not todo:
            return JSONResponse(status_code=404, content={"error": {"code": 404, "message": f"Todo not found with id {id}"}})
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/edit/todo/{id}", response_model=Todo)
def edit_todo(
    id: int,
    todo_update: Todo,
    session: Session = Depends(get_session),
):
    """
    Edit and return the todo

    Args:
        id (int): ID of the todo to edit
        todo_update (TodoUpdate): Updated todo data

    Returns:
        Todo: Updated todo item
    """
    existing_todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if not existing_todo:
        raise HTTPException(status_code=404, detail=f"Todo not found with id {id}")

    if todo_update.title is not None:
        existing_todo.title = todo_update.title
    if todo_update.completed is not None:
        existing_todo.completed = todo_update.completed

    try:
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return existing_todo


@app.delete('/delete/todo/{todo_id}', response_model=Todo)
def delete_todo(todo_id: int, session: Session = Depends(get_session)) -> JSONResponse:
    """
    Delete a todo by ID

    Args:
        todo_id (int): ID of the todo to delete

    Returns:
        JSONResponse: Deleted Todo or error message
    """
    try:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found")

        session.delete(todo)
        session.commit()
        return JSONResponse(status_code=200, content={"detail": f"Todo with ID {todo_id} deleted successfully"})
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
