from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Security,
    BackgroundTasks,
    Request,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from random import randint

from cor_auth.database.db import get_db
from cor_auth.schemas import (
    UserModel,
    ResponseUser,
    TokenModel,
    EmailSchema,
    VerificationModel,
    ChangePasswordModel,
)
from cor_auth.repository import users as repository_users
from cor_auth.services.auth import auth_service
from cor_auth.services.email import send_email_code
from cor_auth.conf.config import settings

router = APIRouter(prefix="/auth", tags=["Authorization"])
security = HTTPBearer()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm


@router.post(
    "/signup", response_model=ResponseUser, status_code=status.HTTP_201_CREATED
)
async def signup(
    body: UserModel,
    db: Session = Depends(get_db),
):
    """
    The signup function creates a new user in the database.
        It takes an email and password as input, hashes the password, and stores it in the database.
        If there is already a user with that email address, it returns an error message.

    :param body: UserModel: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :return: A dict, but the function expects a usermodel
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    print(f"{body.email} user successfully created")
    return {"user": new_user, "detail": "User successfully created"}


@router.post(
    "/login",
    response_model=TokenModel,
)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    The login function is used to authenticate a user.

    :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: Session: Get the database session
    :return: A dictionary with the access_token, refresh_token and token type
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    access_token = await auth_service.create_access_token(
        data={"id": user.id}, expires_delta=3600
    )
    refresh_token = await auth_service.create_refresh_token(data={"id": user.id})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get(
    "/refresh_token",
    response_model=TokenModel,
)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    """
    The refresh_token function is used to refresh the access token.
    It takes in a refresh token and returns an access_token, a new refresh_token, and the type of token (bearer).


    :param credentials: HTTPAuthorizationCredentials: Get the credentials from the request header
    :param db: Session: Pass the database session to the function
    :return: A new access token and a new refresh token
    """
    token = credentials.credentials
    id = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_uuid(id, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_access_token(data={"id": user.id})
    refresh_token = await auth_service.create_refresh_token(data={"id": user.id})
    user.refresh_token = refresh_token
    db.commit()
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# Маршрут для отправки кода подтверждения на почту пользователя
@router.post("/send_verification_code")
async def send_verification_code(
    body: EmailSchema,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    verification_code = randint(100000, 999999)

    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        print("Account already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )

    if exist_user == None:
        background_tasks.add_task(
            send_email_code, body.email, request.base_url, verification_code
        )
        print("Check your email for verification code.")
        await repository_users.write_verification_code(
            email=body.email, db=db, verification_code=verification_code
        )

    return {"message": "Check your email for verification code."}


# Маршрут подтверждения почты/кода
@router.post("/confirm_email")
async def send_verification_code(
    body: VerificationModel, db: Session = Depends(get_db)
):

    ver_code = await repository_users.verify_verification_code(
        body.email, db, body.verification_code
    )
    if ver_code:
        print("Your email is confirmed")
        return True
    else:
        print("Invalid verification code")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid verification code"
        )


# forgot password route
"""
Забыли пароль -> ввод почты -> отправка кода на почту -> ввод кода -> ввод нового пароля (может повторный ввод пароля и сравнение)
"""


@router.post("/forgot password")
async def forgot_password(
    body: EmailSchema,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):

    verification_code = randint(100000, 999999)
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if exist_user:
        background_tasks.add_task(
            send_email_code, body.email, request.base_url, verification_code
        )
        await repository_users.write_verification_code(
            email=body.email, db=db, verification_code=verification_code
        )
    return {"message": "Check your email for verification code."}


@router.patch("/change password")
async def change_password(body: ChangePasswordModel, db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        if body.password == body.confirmed_password:
            await repository_users.change_user_password(body.email, body.password, db)
            return {"message": f"User {body.email} if changed his password"}
        else:
            print("Incorrect password input")
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Incorrect password input",
            )
