"""
FastAPI todo app Schema (SQLModel)
"""

from sqlmodel import SQLModel,Field

class Todo(SQLModel,table=True):
    """
    Todo app schema
    """
    id : int = Field(default=None,primary_key=True)
    title : str = Field(index=True)
    completed: bool = Field(default=True)

