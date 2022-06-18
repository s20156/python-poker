from sqlalchemy import Column, Integer, ForeignKey, String, Float

from utils.Base import Base


class Room(Base):
    __tablename__ = "rooms"
    id = Column("id", Integer, primary_key=True)
    owner_id = Column("owner_id", Integer, ForeignKey("users.id"))
    password = Column("password", String)


class Topic(Base):
    __tablename__ = "topic"
    id = Column("id", Integer, primary_key=True)
    room_id = Column("room_id", Integer, ForeignKey("room.id"))
    value = Column("value", Float)