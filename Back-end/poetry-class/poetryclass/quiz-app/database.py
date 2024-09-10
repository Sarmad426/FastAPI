"""
FastAPI quiz app database connection
"""

from sqlmodel import create_engine


DB_FILE_NAME: str = "quiz.db"

DATABASE = f"sqlite:///{DB_FILE_NAME}"

connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE, echo=True, connect_args=connect_args)
