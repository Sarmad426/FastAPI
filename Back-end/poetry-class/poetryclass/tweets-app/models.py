from sqlmodel import SQLModel, Field
from typing import Optional


class Tweet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    image_filename: Optional[str] = None
