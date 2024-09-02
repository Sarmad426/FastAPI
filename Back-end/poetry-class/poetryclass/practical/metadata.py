"""
Fast API metadata and tags
"""

from fastapi import FastAPI

description = """
Myapp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    title="Sarmad's app",
    description=description,
    summary="Sarmad's favorite app.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Sarmad Rafique",
        "url": "https://sarmad-portfolio.vercel.app/",
        "email": "sarmadrafique040@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT"
    },
    openapi_tags=tags_metadata
)


@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]