# Metadata and docs urls

```py
from fastapi import FastAPI

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Sarmad Rafique",
        "url": "https://sarmad-portfolio.vercel.app",
        "email": "sarmadrafique040@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT"
    },
)


@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]
```

**Tip:**
> You can write Markdown in the description field and it will be rendered in the output.

## Metadata for tags

You can also add additional metadata for the different tags used to group your path operations with the parameter `openapi_tags`.

It takes a list containing one dictionary for each tag.

Each dictionary can contain:

- `name` (required): a `str` with the same tag name you use in the `tags` parameter in your path operations and `APIRouter`s.
- `description`: a `str` with a short description for the tag. It can have Markdown and will be shown in the docs UI.
- `externalDocs`: a `dict` describing external documentation with:
  - `description`: a `str` with a short description for the external docs.
  - `url` (required): a `str` with the URL for the external documentation.

### Create metadata for tags

Let's try that in an example with tags for `users` and `items`.

Create metadata for your tags and pass it to the `openapi_tags` parameter:

```py
from fastapi import FastAPI

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

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]
```

Notice that you can use Markdown inside of the descriptions, for example "login" will be shown in bold (**login**) and "fancy" will be shown in italics (*fancy*).

**Tip:**
> You don't have to add metadata for all the tags that you use.

Docs: <https://fastapi.tiangolo.com/tutorial/metadata/>
