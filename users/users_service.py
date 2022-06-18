import re
from sqlite3 import Cursor
from typing import List

import bcrypt
from sqlalchemy import select, insert, delete

from database.database import get_database_orm
from database.users_model import User

LOGIN_RE = r'^[a-zA-Z0-9]+$'


def validate_login(login: str):
    if not len(login) > 3:
        return False

    return re.match(LOGIN_RE, login) is not None


def validate_password(password):
    return len(password) > 4


async def has_user(login: str):
    async with get_database_orm() as session:
        return (await session.execute(
            select(User).where(User.login == login))).scalars().first()


async def login(login: str, password: str):
    async with get_database_orm() as session:
        user = (await session.execute(select(User).where(User.login == login))).scalars().first()
        if user is None:
            return None
        print(user)
        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode('utf-8')):
            return None
        return user


async def create_user(login: str, password):
    async with get_database_orm() as session:
        async with session.begin():
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            user = User(login=login, password=password)
            session.add(user)


async def get_all_users() -> List[User]:
    async with get_database_orm() as session:
        return (await session.execute(select(User))).scalars()


async def remove_user(login):
    async with get_database_orm() as session:
        return await session.execute(delete(User).where(User.login == login))
