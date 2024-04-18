import enum

from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import declarative_base, Mapped
from cor_auth.database.db import engine

Base = declarative_base()


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    access_token = Column(String(250), nullable=True)
    refresh_token = Column(String(250), nullable=True)
    confirmed = Column(Boolean, default=False)
    role: Mapped[Enum] = Column("role", Enum(Role), default=Role.admin)

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    record = Column(String(100), nullable= False)

Base.metadata.create_all(bind=engine)


