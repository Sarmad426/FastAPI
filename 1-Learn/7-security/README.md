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
