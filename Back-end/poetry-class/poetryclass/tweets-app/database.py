from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./tweets.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_db() -> Session:
    """
    Dependency to get the database session.
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """
    Create the database tables.
    """
    SQLModel.metadata.create_all(engine)
