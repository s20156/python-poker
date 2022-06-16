import jwt
import json
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response, JSONResponse

from commands import users_commands
from commands.users_commands import register, WrongDataException, UserExistsException, get_users, \
    UsersListNotAvailableException
from database.database import get_database
from authorization import generate_jwt, decode_jwt


class Login(HTTPEndpoint):
    async def post(self, request):
        body = await request.json()

        if 'login' not in body or 'password' not in body:
            return Response(JSONResponse({}).body, status_code=400)

        db = get_database()

        out = users_commands.login(db, body['login'], body['password'])
        if out is None:
            return Response(JSONResponse({}).body, status_code=401)

        jwt = generate_jwt(out.id)

        return JSONResponse({"token": jwt})


class Register(HTTPEndpoint):
    async def post(self, request):
        body = await request.json()

        if 'login' not in body or 'password' not in body:
            return Response(JSONResponse({"error": "wrong_data"}).body, status_code=400)

        try:
            register(get_database(), body['login'], body['password'])
        except WrongDataException:
            return Response(JSONResponse({"error": "wrong_data"}).body, status_code=400)
        except UserExistsException:
            return Response(JSONResponse({"error": "existing_user"}).body, status_code=400)

        return JSONResponse({})


class List(HTTPEndpoint):
    async def get(self, request):
        # TODO: Extract to function!!
        if 'authorization' not in request.headers:
            return Response(JSONResponse({}).body, status_code=403)

        token: str = request.headers['authorization']
        token = token.split(" ")[1]
        user_id = decode_jwt(token)

        if user_id is None:
            return Response(JSONResponse({}).body, status_code=403)

        try:
            users = json.dumps(get_users(get_database(), filter), default=lambda o: o.__dict__)
            return JSONResponse(users, status_code=200)
        except UsersListNotAvailableException:
            return Response(JSONResponse({"error": "users_list_not_available"}).body, status_code=500)


class Refresh(HTTPEndpoint):
    async def post(self, request):
        if 'authorization' not in request.headers:
            return Response(JSONResponse({}).body, status_code=403)

        token: str = request.headers['authorization']
        if not token.startswith("JWT "):
            return Response(JSONResponse({}).body, status_code=403)

        token = token[4:]
        user_id = decode_jwt(token)

        if user_id is None:
            return Response(JSONResponse({}).body, status_code=403)

        return JSONResponse({token: generate_jwt(user_id)})
