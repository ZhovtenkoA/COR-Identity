from sqlalchemy.orm import Session
import uuid

from cor_auth.database.models import User, Role
from cor_auth.schemas import UserModel
from sqlalchemy import func


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    The get_user_by_email function takes in an email and a database session,
    then returns the user with that email.

    :param email: str: Pass in the email of the user that we want to get
    :param db: Session: Pass the database session to the function
    :return: The first user found with the email specified
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object containing the information to be added to the database.
            db (Session): The SQLAlchemy Session object used for querying and updating data in the database.
        Returns:
            User: A User object representing a newly created user.

    :param body: UserModel: Pass the data from the request body into our create_user function
    :param db: Session: Create a database session
    :return: A user object
    """

    new_user = User(**body.model_dump())
    new_user.id = str(uuid.uuid4())
    new_user.role = Role.user

    users_count = db.query(func.count(User.id)).scalar()

    if users_count == 0:
        new_user.role = Role.admin
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise e


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user that is being updated
    :param token: str | None: Pass the token to the function
    :param db: Session: Commit the changes to the database
    :return: None, so the return type should be none
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function sets the confirmed field of a user to True.

    :param email: str: Pass the email address of the user to be confirmed
    :param db: Session: Pass the database session into the function
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def get_users(skip: int, limit: int, db: Session) -> list[User]:
    """
    The get_users function returns a list of all users from the database.

    :param skip: int: Skip the first n records in the database
    :param limit: int: Limit the number of results returned
    :param db: Session: Pass the database session to the function
    :return: A list of all users
    """
    query = db.query(User).offset(skip).limit(limit).all()
    return query


async def make_user_role(email: str, role: Role, db: Session) -> None:
    """
    The make_user_role function takes in an email and a role, and then updates the user's role to that new one.
    Args:
    email (str): The user's email address.
    role (Role): The new Role for the user.

    :param email: str: Get the user by email
    :param role: Role: Set the role of the user
    :param db: Session: Pass the database session to the function
    :return: None
    """

    user = await get_user_by_email(email, db)
    user.role = role
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
