from typing import List

from fastapi import Request, Depends, HTTPException, status

from cor_auth.database.models import Role, User
from cor_auth.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self, request: Request, user: User = Depends(auth_service.get_current_user)
    ):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden operation"
            )


free_access = RoleAccess([Role.admin, Role.moderator, Role.user])
admin_moderator = RoleAccess([Role.admin, Role.moderator])
admin_user = RoleAccess([Role.admin, Role.user])
admin = RoleAccess([Role.admin])
