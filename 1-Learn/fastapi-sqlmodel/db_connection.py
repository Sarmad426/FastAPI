"""
FastAPI SQLModel app database connection
"""

from sqlmodel import create_engine, SQLModel, Session


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Returns database session
    """
    with Session(engine) as session:
        yield session
