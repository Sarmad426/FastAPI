"""
Posts app main file
"""

from typing import List, Optional
from pathlib import Path
from fastapi import FastAPI, Depends, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select


from database import create_db_and_tables, get_db
from models import Tweet
from utils import save_image_locally

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allowing all origins (http://localhost:3000)
    allow_credentials=True,  # Allowing credentials (cookies, HTTP Authentication) to be sent to the frontend
    allow_methods=["*"],  # Allowing all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allowing all headers (Authorization, Content-Type, etc.)
)


create_db_and_tables()

UPLOAD_FOLDER = Path("uploads")


@app.post("/tweets/", response_model=Tweet)
async def create_tweet(
    text: str = Form(...),
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db),
):
    """
    API to create a new tweet with an optional image.
    """
    if image and not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

    image_filename = save_image_locally(image) if image else None
    tweet = Tweet(text=text, image_filename=image_filename)
    db.add(tweet)
    db.commit()
    db.refresh(tweet)

    return tweet


@app.get("/tweets/", response_model=List[Tweet])
async def get_tweets(db: Session = Depends(get_db)):
    """
    API to fetch all tweets.
    """
    tweets = db.exec(select(Tweet)).all()

    # Add full URL to image filenames if they exist
    for tweet in tweets:
        if tweet.image_filename:
            tweet.image_filename = f"/uploads/{tweet.image_filename}"
    return tweets


@app.get("/uploads/{filename}")
async def get_image(filename: str):
    """
    Serve uploaded images.
    """
    file_path = UPLOAD_FOLDER / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)


@app.put("/tweets/{tweet_id}", response_model=Tweet)
async def update_tweet(
    tweet_id: int,
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db),
):
    """
    API to update a tweet by its ID. Allows updating the text and/or the image.
    """
    tweet = db.get(Tweet, tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    # Update text if provided
    if text is not None:
        tweet.text = text

    # Update image if provided
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, detail="Uploaded file is not an image."
            )

        # Delete the old image if it exists
        if tweet.image_filename:
            old_image_path = UPLOAD_FOLDER / tweet.image_filename
            if old_image_path.exists():
                old_image_path.unlink()

        # Save the new image
        tweet.image_filename = save_image_locally(image)

    db.add(tweet)
    db.commit()
    db.refresh(tweet)
    return tweet


@app.delete("/tweets/{tweet_id}", status_code=204)
async def delete_tweet(tweet_id: int, db: Session = Depends(get_db)):
    """
    API to delete a tweet by its ID.
    """
    tweet = db.get(Tweet, tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    # Delete the associated image if it exists
    if tweet.image_filename:
        image_path = UPLOAD_FOLDER / tweet.image_filename
        if image_path.exists():
            image_path.unlink()

    db.delete(tweet)
    db.commit()
    return {"detail": "Tweet deleted successfully"}
