"""
FastAPI todo app database connection
"""

from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, create_engine

database :str = 'todos.db'

connection_string : str = f'sqlite:///{database}'


engine = create_engine(connection_string,echo=True,connect_args={'check_same_thread':False})

def create_db_and_tables():
    """
    Creates database and tables on start
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Connection session
    """
    with Session(engine) as session:
        yield session