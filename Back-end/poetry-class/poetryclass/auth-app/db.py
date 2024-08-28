from sqlmodel import SQLModel, create_engine,Field,Session

DB_URL = "sqlite:///auth_app.db"


engine=create_engine(DB_URL, echo=True)

class User(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    role: str

class UserCreate(SQLModel):
    name: str
    email: str
    password: str
    role: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session