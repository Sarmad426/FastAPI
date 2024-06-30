"""
FastAPI todo app schemas
"""

from sqlmodel import SQLModel, Field
from typing import Optional


class Todo(SQLModel, table=True):
    """
    Todo schema (SQLModel)
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = False
