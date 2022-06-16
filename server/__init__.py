import jwt
from jwt import ExpiredSignatureError
from starlette.applications import Starlette
from starlette.authentication import AuthenticationBackend, AuthenticationError, AuthCredentials, SimpleUser
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Mount

from server.api import api_routes


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "authorization" not in conn.headers:
            return
        auth = conn.headers["authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "jwt":
                return
            decoded = jwt.decode(credentials, 'secret', algorithms="HS256")
        except ExpiredSignatureError:
            raise AuthenticationError("Expired JWT")

        user_id = decoded.get("sub")
        return AuthCredentials(["authenticated"], SimpleUser(user_id))


routes = [
    Mount("/api", routes=api_routes, name="api"),
]


def run():
    middleware = [
        Middleware(AuthenticationMiddleware, backend=BasicAuthBackend()),
        Middleware(TrustedHostMiddleware, allowed_hosts=['*']),
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']),
    ]
    app = Starlette(True, routes, middleware=middleware)

    return app