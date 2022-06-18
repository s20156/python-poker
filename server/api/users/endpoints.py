import jwt
import json
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response, JSONResponse

from commands import users_commands
from commands.users_commands import register, WrongDataException, UserExistsException, get_users, \
    UsersListNotAvailableException, delete_user
from database.database import get_database, get_database_orm
from authorization import generate_jwt, decode_jwt


class Login(HTTPEndpoint):
    async def post(self, request):
        body = await request.json()

        if 'login' not in body or 'password' not in body:
            return Response(JSONResponse({}).body, status_code=400)

        out = await users_commands.login(body['login'], body['password'])
        print(out)
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
            await register(body['login'], body['password'])
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
            data = await get_users()
            users = []
            for user in data:
                users.append(user.login)
            return JSONResponse(users, status_code=200)
        except UsersListNotAvailableException:
            return Response(JSONResponse({"error": "users_list_not_available"}).body, status_code=500)

    async def delete(self, request):
        if 'authorization' not in request.headers:
            return Response(JSONResponse({}).body, status_code=403)

        token: str = request.headers['authorization']
        token = token.split(" ")[1]
        user_id = decode_jwt(token)

        if user_id is None:
            return Response(JSONResponse({}).body, status_code=403)

        body = await request.json()

        if 'login' not in body:
            return Response(JSONResponse({"error": "wrong_data"}).body, status_code=400)

        try:
            await delete_user(body["login"])
        except WrongDataException:
            return Response(JSONResponse({"error": "wrong_data"}).body, status_code=400)


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
