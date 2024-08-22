# Security

## OAuth2

OAuth2 is a specification that defines several ways to handle authentication and authorization.

It is quite an extensive specification and covers several complex use cases.

It includes ways to authenticate using a "third party".

That's what all the systems with "login with Facebook, Google, Twitter, GitHub" use underneath.

### OpenID Connect

OpenID Connect is another specification, based on OAuth2.

It just extends OAuth2 specifying some things that are relatively ambiguous in OAuth2, to try to make it more interoperable.

For example, Google login uses OpenID Connect (which underneath uses OAuth2).

But Facebook login doesn't support OpenID Connect. It has its own flavor of OAuth2.

### OpenAPI

OpenAPI (previously known as Swagger) is the open specification for building APIs (now part of the Linux Foundation).

**FastAPI** is based on **OpenAPI**.

That's what makes it possible to have multiple automatic interactive documentation interfaces, code generation, etc.

OpenAPI has a way to define multiple security "schemes".

By using them, you can take advantage of all these standard-based tools, including these interactive documentation systems.

OpenAPI defines the following security schemes:

- `apiKey`: an application specific key that can come from:
  - A query parameter.
  - A header.
  - A cookie.
- `http`: standard HTTP authentication systems, including:
  - bearer: a header `Authorization` with a value of `Bearer` plus a token. This is inherited from OAuth2.
  - HTTP Basic authentication.
  - HTTP Digest, etc.
- `oauth2`: all the OAuth2 ways to handle security (called "flows").
  - Several of these flows are appropriate for building an OAuth 2.0 authentication provider (like Google, Facebook, Twitter, GitHub, etc):
  - `implicit`
  - `clientCredentials`
  - `authorizationCode`
- But there is one specific "flow" that can be perfectly used for handling authentication in the same application directly:
  - `password`: some next chapters will cover examples of this.
- `openIdConnect`: has a way to define how to discover OAuth2 authentication data automatically.
This automatic discovery is what is defined in the OpenID Connect specification.

Docs: <https://fastapi.tiangolo.com/tutorial/security/>

## First Steps

Let's imagine that you have your backend API in some domain.

And you have a frontend in another domain or in a different path of the same domain (or in a mobile application).

And you want to have a way for the frontend to authenticate with the backend, using a username and password.

We can use OAuth2 to build that with FastAPI.

**Info:**
> First make sure `python-multipart` is installed. If you have used `pip install "fastapi[standard]"` it will be installed automatically. But if you run `pip install fastapi` you have to manually install it. Make sure the virtual environment is activated while installing it.

Using poetry:

```py
poetry add python-multipart
```

This is because **OAuth2** uses "form data" for sending the `username` and `password`.

### Create `main.py` file

```py
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

**Run it:**

```bash
uvicorn main:app --reload
```

**Info:**
> You already have a shiny new "Authorize" button. And your path operation has a little lock in the top-right corner that you can click. And if you click it, you have a little authorization form to type a `username` and `password` (and other optional fields):

It doesn't matter what you type in the form, it won't work yet. But we'll get there.

**Must Read**: <https://fastapi.tiangolo.com/tutorial/security/first-steps/#the-password-flow>

### Password Flow

Now let's go back a bit and understand what is all that.

The `password` "flow" is one of the ways ("flows") defined in OAuth2, to handle security and authentication.

**OAuth2** was designed so that the backend or API could be independent of the server that authenticates the user.

But in this case, the same **FastAPI** application will handle the API and the authentication.

So, let's review it from that simplified point of view:

- The user types the `username` and `password` in the frontend, and hits Enter.
- The frontend (running in the user's browser) sends that `username` and `password` to a specific URL in our API (declared with tokenUrl="token").
- The API checks that `username` and `password`, and responds with a "token" (we haven't implemented any of this yet).
  - A "token" is just a string with some content that we can use later to verify this user.
  - Normally, a token is set to expire after some time.
    - So, the user will have to log in again at some point later.
    - And if the token is stolen, the risk is less. It is not like a permanent key that will work forever (in most of the cases).
- The frontend stores that token temporarily somewhere.
- The user clicks in the frontend to go to another section of the frontend web app.
- The frontend needs to fetch some more data from the API.
  - But it needs authentication for that specific endpoint.
  - So, to authenticate with our API, it sends a header `Authorization` with a value of `Bearer` plus the token.
  - If the token contains `foobar`, the content of the `Authorization` header would be: `Bearer foobar`.

### FastAPI's `OAuth2PasswordBearer`

In this example we are going to use **OAuth2**, with the **Password** flow, using a **Bearer** token. We do that using the `OAuth2PasswordBearer` class.

**Info:**
> A "bearer" token is not the only option. But it's the best one for our use case. And it might be the best for most use cases, unless you are an OAuth2 expert and know exactly why there's another option that suits better your needs. In that case, FastAPI also provides you with the tools to build it.

When we create an instance of the `OAuth2PasswordBearer` class we pass in the `tokenUrl` parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the `username` and `password` in order to get a token.

```py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

**Tip:**
> Here `tokenUrl="token"` refers to a relative URL `token` that we haven't created yet. As it's a relative URL, it's equivalent to `./token`.
> Because we are using a relative URL, if your API was located at `https://example.com/`, then it would refer to `https://example.com/token`. But if your API was located at `https://example.com/api/v1/`, then it would refer to `https://example.com/api/v1/token`.
> Using a relative URL is important to make sure your application keeps working even in an advanced use case like [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/).

This parameter doesn't create that endpoint / path operation, but declares that the URL `/token` will be the one that the client should use to get the token. That information is used in OpenAPI, and then in the interactive API documentation systems.

The `oauth2_scheme` variable is an instance of `OAuth2PasswordBearer`, but it is also a "callable".

```py
oauth2_scheme(some, parameters)
```

So it can be used with `Depends`.

```py
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
```

**What it does:**

It will go and look in the request for that `Authorization` header, check if the value is `Bearer` plus some token, and will return the token as a `str`.

If it doesn't see an `Authorization` header, or the value doesn't have a `Bearer` token, it will respond with a 401 status code error (`UNAUTHORIZED`) directly.

You don't even have to check if the token exists to return an error. You can be sure that if your function is executed, it will have a `str` in that token.

Docs: <https://fastapi.tiangolo.com/tutorial/security/first-steps/>

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
