from database.users_model import User
from users import users_service


class RegisterException(Exception):
    pass


class WrongDataException(RegisterException):
    pass


class UserExistsException(RegisterException):
    pass


class UsersListNotAvailableException(Exception):
    pass


async def register(login, password):
    if not users_service.validate_login(login):
        raise WrongDataException("Wrong login")

    if not users_service.validate_password(password):
        raise WrongDataException("Wrong password")

    if await users_service.has_user(login) is not None:
        raise UserExistsException("User exists")

    await users_service.create_user(login, password)


async def login(login, password) -> User:
    return await users_service.login(login, password)


async def get_users():
    return await users_service.get_all_users()


async def delete_user(login):
    if await users_service.has_user(login) is None:
        raise UserExistsException("User does not exist")
    return await users_service.remove_user(login)
