"""
Auth app database connection
"""

from sqlmodel import SQLModel, create_engine, Field, Session

DB_URL = "sqlite:///auth_app.db"


engine = create_engine(DB_URL, echo=True)


class User(SQLModel, table=True):
    """
    User model
    """

    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    role: str


class UserCreate(SQLModel):
    """
    User create model
    """

    name: str
    email: str
    password: str
    role: str


def create_db_and_tables():
    """
    Creates db and tables
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Yields database session
    """
    with Session(engine) as session:
        yield session
