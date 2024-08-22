# Fast API Security Oauth2

## Simple Oauth2 with Password and Bearer

### Get the `username` and `password`

We are going to use FastAPI security utilities to get the `username` and `password`.

OAuth2 specifies that when using the "password flow" (that we are using) the client/user must send a `username` and `password` fields as form data.

**`scope`**

The spec also says that the client can send another form field "`scope`".

The form field name is `scope` (in singular), but it is actually a long string with "scopes" separated by spaces.

Each "scope" is just a string (without spaces).

They are normally used to declare specific security permissions, for example:

- `users:read` or `users:write` are common examples.
- `instagram_basic` is used by Facebook / Instagram.
- `https://www.googleapis.com/auth/drive` is used by Google.

**Info:**
> In OAuth2 a "scope" is just a string that declares a specific permission required.
> It doesn't matter if it has other characters like : or if it is a URL.
> Those details are implementation specific.For OAuth2 they are just strings.

### Get `username` and `password`

**`OAuth2PasswordRequestForm`**

import `OAuth2PasswordRequestForm`, and use it as a dependency with `Depends` in the path operation for `/token`:

```py
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
```

`OAuth2PasswordRequestForm` is a class dependency that declares a form body with:

- The `username`.
- The `password`.
- An optional `scope` field as a big string, composed of strings separated by spaces.
- An optional `grant_type`.
- An optional `client_id` (we don't need it for our example).
- An optional `client_secret` (we don't need it for our example).

Now, get the user data from the (fake) database, using the `username` from the form field.

If there is no such user, we return an error saying "Incorrect username or password".

For the error, we use the exception `HTTPException`:

```py
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
```

#### Fake password hashing

```py
user = UserInDB(**user_dict)
hashed_password = fake_hash_password(form_data.password)
if not hashed_password == user.hashed_password:
    raise HTTPException(status_code=400, detail="Incorrect username or password")
```

#### Return the token

The response of the `token` endpoint must be a JSON object.

It should have a `token_type`. In our case, as we are using "Bearer" tokens, the token type should be `"bearer"`.

And it should have an `access_token`, with a string containing our access token.

For this simple example, we are going to just be completely insecure and return the same `username` as the token.s

```py
 return {"access_token": user.username, "token_type": "bearer"}
```

**Tip:**
> By the spec, you should return a JSON with an `access_token` and a `token_type`, the same as in this example.
> This is something that you have to do yourself in your code, and make sure you use those JSON keys.

### Update the dependencies

We want to get the `current_user` only if this user is active.

So, we create an additional dependency `get_current_active_user` that in turn uses `get_current_user` as a dependency.

Both of these dependencies will just return an HTTP error if the user doesn't exist, or if is inactive.

So, in our endpoint, we will only get a user if the user exists, was correctly authenticated, and is active:

```py
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### Authenticate

Run the app and open <http://127.0.0.1:8000/docs>

Click the "Authorize" button.

Use the credentials:

User: `johndoe`

Password: `secret`

You will be authenticated. You can get current user data as `json` from the `get` route.

If you click the lock icon and logout, and then try the same operation again, you will get an HTTP 401 error of:

```json
{
  "detail": "Not authenticated"
}
```

**Inactive user:**

Now try with an inactive user, authenticate with:

User: `alice`

Password: `secret2`

And try to use the operation `GET` with the path `/users/me`.

You will get an "Inactive user" error, like:

```json
{
  "detail": "Inactive user"
}
```

Docs: <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>
