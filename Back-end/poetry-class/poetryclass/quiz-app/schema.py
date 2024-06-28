"""
FastAPI quiz app Database schema
"""

from sqlmodel import SQLModel, Session, Field,Integer, Column, JSON
from database import engine

class Quiz(SQLModel,table=True):
    """
    Quiz schema
    """
    id : int = Field(default=None,primary_key=True)
    question : str = Field(index=True)
    options: list[str] = Field(sa_column=Column("options", JSON))
    correct_option: int = Field(sa_column=Column("correct_option", Integer))

class Points(SQLModel, table=True):
    """
    Credit points counter
    """
    id : int = Field(default=None, primary_key=True)
    points : int = Field(default=0)


def get_session():
    """
    Returns the database session
    """
    with Session(engine) as session:
        yield session
