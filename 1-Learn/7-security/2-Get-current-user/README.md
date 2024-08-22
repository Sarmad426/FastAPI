# Fast API Security Oauth2

## Get Current User

### Create a user model

First, let's create a Pydantic user model.

```py
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
```

### Create a `get_current_user` dependency

Dependency `get_current_user` will receive a `token` as a `str` from the sub-dependency `oauth2_scheme`.

```py
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
```

### Get the user

`get_current_user` will use a (fake) utility function we created, that takes a token as a `str` and returns our Pydantic `User` model:

```py
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user
```

### Inject the current user

So now we can use the same `Depends` with our `get_current_user` in the path operation:

```py
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
```

Docs: <https://fastapi.tiangolo.com/tutorial/security/get-current-user/>
