from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Session,select
from sqlalchemy.orm import selectinload

from db import engine, get_session
from schema import User,Post


app = FastAPI(title="SQLModel Relationships")

@app.on_event('startup')
def create_db_and_tables():
    """
    Creates database and tables
    """
    SQLModel.metadata.create_all(engine)

@app.post('/user/new', response_model=User)
def create_user(session:Annotated[Session,Depends(get_session)],user: User):
    """Create new user

    Args:
        user (User): New user
    """
    user = User(name=user.name, email=user.email)
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
    except Exception as e:
        # Undo partial changes if error happens
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return user

@app.get('/users')
def get_users(session:Annotated[Session,Depends(get_session)]):
    """Get all users

    Returns:
        List[User]: List of users
    """
    try:
        query = select(User)
        users : list[User] = session.exec(query).all()
        if not users:
            return JSONResponse(status_code=404, content={"error": {"code": 404, "message": "No users in the database"}})
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post('/post/new',response_model=Post)
def create_post(session:Annotated[Session,Depends(get_session)],post:Post):
    """Create new post

    Args:
        post (Post): New post
    """
    new_post = Post(title=post.title,content=post.content,user_id=post.user_id)
    session.add(new_post)
    try:
        session.commit()
        session.refresh(new_post)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return new_post


@app.get('/posts')
def get_posts(session:Annotated[Session,Depends(get_session)]):
    """Get all users

    Returns:
        List[User]: List of users
    """
    try:
        query = select(Post)
        posts : list[User] = session.exec(query).all()
        if not posts:
            return JSONResponse(status_code=404, content={"error": {"code": 404, "message": "No posts in the database"}})
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users_with_posts", response_model=list[User])
def get_users_with_posts(*, session: Session = Depends(get_session)):
    statement = select(User).select_from(Post).join(User,User.id == Post.user_id)
    users = session.exec(statement).all()
    return users
