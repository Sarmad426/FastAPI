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
