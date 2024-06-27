"""
FastAPI todo app Database connection
"""

from sqlmodel import Session, create_engine

DB_FILE: str = "todos.db"

DATABASE: str = f"sqlite:///{DB_FILE}"

connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE, echo=True, connect_args=connect_args)


def get_session():
    """
    Returns database session
    """
    with Session(engine) as session:
        yield session
