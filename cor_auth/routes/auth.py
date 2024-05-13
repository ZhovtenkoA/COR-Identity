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
from cor_auth.database.models import Verification
from cor_auth.schemas import UserModel, ResponseUser, TokenModel, EmailSchema, VerificationModel, ChangePasswordModel
from cor_auth.repository import users as repository_users
from cor_auth.services.auth import auth_service
from cor_auth.services.email import send_email, send_email_code
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
    background_tasks: BackgroundTasks,
    request: Request,
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
    # background_tasks.add_task(
    #     send_email,
    #     new_user.email,
    #     request.base_url,
    # )
    return {"user": new_user, "detail": "User successfully created"}


@router.post(
    "/login",
    response_model=TokenModel,
    description="No more than 10 requests per minute",
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
    # if not user.confirmed:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed"
    #     )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    access_token = await auth_service.create_access_token(
        data={"sub": user.email}, expires_delta=3600
    )
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get(
    "/refresh_token",
    response_model=TokenModel,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
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
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    user.refresh_token = refresh_token
    db.commit()
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# @router.get("/confirmed_email/{token}")
# async def confirmed_email(token: str, db: Session = Depends(get_db)):
#     """
#     The confirmed_email function is used to confirm a user's email address.
#     It takes the token from the URL and uses it to get the user's email address.
#     Then, it checks if that user exists in our database, and if they do not exist,
#     an HTTP 400 error is raised. If they do exist but their account has already been confirmed,
#     then a message saying so will be returned. Otherwise (if they are found in our database
#     but have not yet confirmed their account), we call repository_users' confirmed_email function
#     with that email as its argument

#     :param token: str: Get the token from the url
#     :param db: Session: Get the database session
#     :return: A json object with a message
#     """
#     email = await auth_service.get_email_from_token(token)
#     user = await repository_users.get_user_by_email(email, db)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
#         )
#     if user.confirmed:
#         return {"message": "Your email is already confirmed"}
#     await repository_users.confirmed_email(email, db)
#     return {"message": "Email confirmed"}


@router.post("/request_email", description="No more than 10 requests per minute")
async def request_email(
    body: EmailSchema,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    The request_email function is used to send an email to the user with a link that will allow them
    to confirm their email address. The function takes in the body of the request, which should be a JSON object
    with one key: &quot;email&quot;. This key's value should be set to the user's email address. If this is not provided,
    the server will return an error message and status code 400 (Bad Request). If it is provided, then we check if
    the user has already confirmed their account by checking if they have been assigned a confirmation token or not.
    If they have already confirmed their account, then

    :param body: EmailSchema: Validate the data sent in the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base url of the server,
    :param db: Session: Pass the database session to the repository layer
    :return: A dict with a message
    """
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(
            send_email,
            user.email,
            request.base_url,
        )
    return {"message": "Check your email for confirmation."}


# Маршрут для отправки кода подтверждения на почту пользователя
@router.post("/send_verification_code")
async def send_verification_code(
    body: EmailSchema,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)):

    verification_code = randint(100000, 999999)

    # verification_entry = repository_users.get_code_record_by_email(body.email, db)
    verification_entry = db.query(Verification).filter(Verification.email == body.email).first()
    if verification_entry:
        print(verification_entry)
        print("Verification code already sent")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Verification code already sent"
        )
    
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    if exist_user and exist_user.confirmed:
        return {"message": "Your email is already confirmed"}
    
    if exist_user == None:
        background_tasks.add_task(
            send_email_code,
            body.email,
            request.base_url,
            verification_code
        )
        await repository_users.write_verification_code(email=body.email, db=db, verification_code=verification_code)

    return {"message": "Check your email for verification code."}

# Маршрут подтверждения почты/кода
@router.post("/confirm_email")
async def send_verification_code(
    body: VerificationModel,
    db: Session = Depends(get_db)):

    ver_code = await repository_users.verify_verification_code(body.email, db, body.verification_code)
    if ver_code:
        return {"message": "Your email is confirmed"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid verification code")
   
    
#forgot password route
"""
Забыли пароль - ввод почты - отправка кода на почту - ввод кода - ввод нового пароля (может повторный ввод пароля и сравнение)
"""

@router.post("/forgot password")
async def forgot_password(
    body: EmailSchema,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)):

    verification_code = randint(100000, 999999)
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if exist_user:
        background_tasks.add_task(
            send_email_code,
            body.email,
            request.base_url,
            verification_code
        )
        await repository_users.write_verification_code(email=body.email, db=db, verification_code=verification_code)
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
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect password input")
