import enum
import uuid

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

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    access_token = Column(String(250), nullable=True)
    refresh_token = Column(String(250), nullable=True)
    # confirmed = Column(Boolean, default=False)
    role: Mapped[Enum] = Column("role", Enum(Role), default=Role.admin)
    # verification_code = Column(Integer, default=None)


class Verification(Base):
    __tablename__ = "verification"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), unique=True, nullable=False)
    verification_code = Column(Integer, default=None)


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    record = Column(String(100), nullable=False)


Base.metadata.create_all(bind=engine)
