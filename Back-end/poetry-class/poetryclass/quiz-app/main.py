"""
FastAPI quiz app entry point
"""

from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select


from schema import Quiz, Points, get_session
from database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Creates the database and the quiz table if it doesn't exist
    """
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


# Allow any origin, credentials, and specific methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow all origins for local development. Change this in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def get_quizzes(session: Annotated[Session, Depends(get_session)]):
    """
    Returns all the quizzes
    """
    quizzes = session.exec(select(Quiz)).all()
    if quizzes:
        return quizzes
    return "No quizzes in the database"


@app.post("/quiz/new")
def create_quiz_question(
    session: Annotated[Session, Depends(get_session)],
    question: str,
    option1: str,
    option2: str,
    option3: str,
    option4: str,
    correct_option: int,
):
    """
    Creates a new quiz question
    """
    options = [option1, option2, option3, option4]

    # Validate correct option
    if correct_option < 0 or correct_option > 3:
        raise ValueError("Correct option should be an index from 0 to 3")
    print("Here is the Question .. ->", question)
    new_quiz = Quiz(question=question, options=options, correct_option=correct_option)
    session.add(new_quiz)
    session.commit()
    session.refresh(new_quiz)
    return new_quiz


@app.post("/quiz/delete")
def delete_quiz_question(session: Annotated[Session, Depends(get_session)], id: int):
    """
    Deletes quiz by id
    """
    quiz = session.exec(select(Quiz).where(Quiz.id == id)).first()
    session.delete(quiz)
    session.commit()
    return quiz


@app.get("/{id}")
def get_quiz_question_by_id(session: Annotated[Session, Depends(get_session)], id: int):
    """
    Returns the quiz question by id
    """
    quiz = session.exec(select(Quiz).where(Quiz.id == id)).first()
    if quiz:
        return quiz
    raise HTTPException(status_code=404, detail=f"Question not found with id {id}")


@app.get("/points/total")
def get_points(session: Annotated[Session, Depends(get_session)]):
    """
    Returns the total points
    """
    points = session.exec(select(Points)).first()
    if points:
        return points
    raise HTTPException(status_code=404, detail="No points found")


@app.patch("/points/update")
def edit_points(session: Annotated[Session, Depends(get_session)], points: int):
    """
    Edit the points counter
    """
    db_points = session.exec(select(Points)).first()
    print("Db points", db_points)
    if db_points:
        db_points.points = points
        session.add(db_points)
        session.commit()
        session.refresh(db_points)
        return db_points
    raise HTTPException(status_code=404, detail="No points found")
