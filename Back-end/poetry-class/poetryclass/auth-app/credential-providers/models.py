from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: Optional[str] = None
    provider: str
    provider_id: str


class UserCreate(BaseModel):
    email: str
    name: Optional[str]
    provider: str
    provider_id: str
