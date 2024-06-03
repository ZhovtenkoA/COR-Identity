from pydantic import BaseModel, Field, EmailStr
from cor_auth.database.models import Role


class UserModel(BaseModel):
    email: str
    password: str = Field(min_length=4, max_length=10)


class UserDb(BaseModel):
    id: str
    email: str
    role: Role

    class Config:
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


class RecordModel(BaseModel):
    record: str = Field(max_length=100)


class RecordResponse(RecordModel):
    id: int
    record: bytes = Field()


class VerificationModel(BaseModel):
    email: EmailStr
    verification_code: int


class ChangePasswordModel(BaseModel):
    email: str
    password: str = Field(min_length=4, max_length=10)
    
