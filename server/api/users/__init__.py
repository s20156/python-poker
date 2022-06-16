from starlette.routing import Route

from server.api.users.endpoints import Login, Register, List, Refresh

users_routes = [
    Route("/login", Login),
    Route("/register", Register),
    Route("/list", List),
    Route('/refresh', Refresh)
]
