from sqlalchemy import Column, Integer, String, ForeignKey
from utils.Base import Base


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    login = Column("login", String, unique=True)
    password = Column("password", String)

