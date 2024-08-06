"""
User posts Database schema
"""

from sqlmodel import SQLModel, Field, ForeignKey, Relationship

class User(SQLModel,table=True):
    """User model
    Args:
    -  id (int): primary key
    -  name (str): user's name
    -  email (str): user's email
    """
    id : int = Field(default=None,primary_key=True)
    name : str = Field(index=True)
    email : str = Field(index=True,unique=True)
    post : list['Post'] = Relationship(back_populates="user")

class Post(SQLModel,table=True):
    """Post model
    Args:
    -  id (int): primary key
    -  title (str): post's title
    -  content (str): post's content
    -  liked: bool = Post liked or not
    -  user_id (int): foreign key referencing User.id
    """
    id : int = Field(default=None,primary_key=True)
    title : str = Field()
    content : str = Field()
    liked : bool = Field(default=False)
    user_id : int | None = Field(default=None, foreign_key='user.id')
    user : User | None = Relationship(back_populates="post")
