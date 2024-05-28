from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from cor_auth.database.db import get_db
from cor_auth.services.auth import auth_service
from cor_auth.database.models import User, Role
from cor_auth.schemas import UserDb
from cor_auth.services.roles import free_access, admin
from cor_auth.repository import users
from pydantic import EmailStr

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/get_all", response_model=list[UserDb], dependencies=[Depends(free_access)]
)
async def get_all_users(
    skip: int = 0,
    limit: int = 10,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    **Get a list of users.**
    This route allows to get a list of pagination-aware users.
    Level of Access:
    - Current authorized user
    :param skip: int: Number of users to skip.
    :param limit: int: Maximum number of users to return.
    :param current_user: User: Current authenticated user.
    :param db: Session: Database session.
    :return: List of users.
    :rtype: List[UserDb]
    """
    list_users = await users.get_users(skip, limit, db)
    return list_users


@router.patch("/asign_role/{role}", dependencies=[Depends(admin)])
async def assign_role(email: EmailStr, role: Role, db: Session = Depends(get_db)):
    """
    **Assign a role to a user by email.**
    This route allows to assign the selected role to a user by their email.
    Level of Access:
    - Administrator
    :param email: EmailStr: Email of the user to whom you want to assign the role.
    :param role: Role: The selected role for the assignment (Administrator, Moderator or User).
    :param db: Session: Database Session.
    :return: Message about successful role change.
    :rtype: dict
    """
    user = await users.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if role == user.role:
        return {"message": "The role has already been assigned to this user"}
    else:
        await users.make_user_role(email, role, db)
        return {"message": f"{email} {role.value}"}
