from fastapi import APIRouter, Request, Depends, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_session
from models import User, UserCreate
import os

router = APIRouter()

config = Config(".env")
oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri="http://localhost:8000/auth/google/callback",
    client_kwargs={'scope': 'openid profile email'},
)

oauth.register(
    name='github',
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri="http://localhost:8000/auth/github/callback",
    client_kwargs={'scope': 'user:email'},
)

def create_or_get_user(session: Session, user_create: UserCreate):
    user = session.query(User).filter(User.email == user_create.email).first()
    if user:
        return user
    user = User.from_orm(user_create)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/login/{provider}")
async def login(request: Request, provider: str):
    redirect_uri = request.url_for(f"{provider}_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.route('/auth/google/callback')
async def google_callback(request: Request, session: Session = Depends(get_session)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    user_create = UserCreate(
        email=user_info['email'],
        name=user_info.get('name'),
        provider='google',
        provider_id=user_info['sub']
    )
    user = create_or_get_user(session, user_create)
    return {"token": token, "user": user}

@router.route('/auth/github/callback')
async def github_callback(request: Request, session: Session = Depends(get_session)):
    token = await oauth.github.authorize_access_token(request)
    user_info = await oauth.github.get('user', token=token)
    user_create = UserCreate(
        email=user_info['email'],
        name=user_info.get('name'),
        provider='github',
        provider_id=str(user_info['id'])
    )
    user = create_or_get_user(session, user_create)
    return {"token": token, "user": user}
