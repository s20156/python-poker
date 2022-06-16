from starlette.routing import Route

from server.api.rooms.endpoints import Rooms, Create, Join

rooms_routes = [
    Route("/rooms", Rooms),
    Route("/create", Create),
    Route("/{id}/join", Join)
]
