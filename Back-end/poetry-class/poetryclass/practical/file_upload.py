"""
Fast Api file upload
"""

from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A File read as bytes")]):
    return {"file_size": f"{len(file)} bytes"}


@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A File read as bytes")]
):
    return {"filename": file.filename, "content_type": file.content_type}
