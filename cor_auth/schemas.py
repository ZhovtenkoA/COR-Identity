from pydantic import BaseModel, Field, EmailStr
from cor_auth.database.models import Role


class UserModel(BaseModel):
    username: str = Field(min_length=4, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    role: Role

    class Config:
        # orm_mode = True
        from_attributes = True


class ResponseUser(BaseModel):
    user: UserDb
    detatil: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class EmailSchema(BaseModel):
    email: EmailStr
