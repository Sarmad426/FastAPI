"""
Image background remover
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rembg import remove
from io import BytesIO
from PIL import Image

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads file
    """
    # Read the image file
    image_data = await file.read()

    # Process the image
    input_image = Image.open(BytesIO(image_data))
    output_image = remove(input_image)
    output_image_bytes = BytesIO()
    output_image.save(output_image_bytes, format="PNG")
    output_image_bytes.seek(0)

    return StreamingResponse(output_image_bytes, media_type="image/png")


# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5100)
