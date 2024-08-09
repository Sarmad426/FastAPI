"""
FastAPI SQL Model ORM relationships database connection
"""

import os
from dotenv import load_dotenv

from sqlmodel import Session, create_engine


load_dotenv()

connect_args = {'check_same_thread':False}

DB_URL = os.getenv('DATABASE_URL')


engine = create_engine(DB_URL,echo=True,connect_args=connect_args)

def get_session():
    """
    Returns database session
    """
    with Session(engine) as session:
        yield session