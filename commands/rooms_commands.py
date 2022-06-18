from rooms import rooms_service


class NoPasswordException(Exception):
    pass


class CantJoinException(Exception):
    pass


class NoRoomException(Exception):
    pass


async def create_room(user_id, password):
    await rooms_service.create_room(user_id, password)


def join_room(db, user_id, room_id, password):
    with db:
        rooms_service.join_room(db, user_id, room_id, password)


def check_room_exists(db, room_id):
    if not rooms_service.get_room(db, room_id):
        return False
