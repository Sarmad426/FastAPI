import os
from uuid import uuid4
from fastapi import UploadFile

UPLOAD_FOLDER = "uploads"


def save_image_locally(image: UploadFile) -> str:
    """
    Saves the uploaded image locally and returns the file name.
    """
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads folder exists

    file_extension = image.filename.split(".")[-1]
    filename = f"{uuid4().hex}.{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as f:  # wb (Write Binary)
        f.write(image.file.read())

    return filename
