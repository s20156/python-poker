import sqlite3

from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, Response

from authorization import decode_jwt
from commands.rooms_commands import create_room, join_room, NoPasswordException
from database.database import get_database


class Rooms(HTTPEndpoint):
    async def get(self, request):
        pass


class My(HTTPEndpoint):
    async def get(self, request):
        pass


class Create(HTTPEndpoint):
    async def post(self, request):
        if 'authorization' not in request.headers:
            return Response(JSONResponse({}).body, status_code=403)

        token: str = request.headers['authorization']
        token = token.split(" ")[1]
        user_id = decode_jwt(token)

        if user_id is None:
            return Response(JSONResponse({}).body, status_code=403)

        try:
            body = await request.json()
            await create_room(user_id, body['password'])
        except NoPasswordException:
            return Response(JSONResponse({}), status_code=400)
        return JSONResponse({})


class Join(HTTPEndpoint):
    async def post(self, request):
        room_id = request.path_params.get('id')
        if "authorization" not in request.headers:
            return Response(JSONResponse({}).body, status_code=403)

        token: str = request.headers['authorization']
        token = token.split(" ")[1]
        user_id = decode_jwt(token)

        if user_id is None:
            return Response(JSONResponse({}).body, status_code=403)

        body = await request.json()

        if room_id is None:
            return Response(JSONResponse({"error": "wrong_route_params"}).body, status_code=400)

        if "password" not in body:
            return Response(JSONResponse({"error": "wrong_data"}).body, status_code=400)

        try:
            await join_room(user_id, room_id, body['password'])
        except sqlite3.IntegrityError:
            return Response(JSONResponse({"error": "user_already_in_room"}).body, status_code=409)
        return JSONResponse({})