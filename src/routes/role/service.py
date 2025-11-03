from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.routes.role.data_access import RoleDataAccessDep
from src.routes.role.schemas import RoleAccessSchema, RoleSchema
from src.routes.user.schemas import UserInDBSchema
from src.routes.user.service import UserServiceDep


class RoleService:
    def __init__(self, data_access: RoleDataAccessDep, user_service: UserServiceDep):
        self.data_access = data_access
        self.user_service = user_service

    async def get_roles_with_permissions(
        self,
        current_user: UserInDBSchema,
    ) -> list[tuple[RoleSchema, RoleAccessSchema]]:
        if not await self.user_service.check_user_permission(
            current_user.id, "read_roles_permission"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission read roles",
            )
        return await self.data_access.get_roles_with_permissions()

    async def get_role_permissions(
        self,
        role_id: int,
        current_user: UserInDBSchema,
    ) -> RoleAccessSchema:
        if not await self.user_service.check_user_permission(
            current_user.id, "read_roles_permission"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission read roles",
            )
        return await self.data_access.get_role_permissions(role_id)

    async def update_role_permissions(
        self,
        role_id: int,
        permissions: RoleAccessSchema,
        current_user: UserInDBSchema,
    ) -> RoleAccessSchema:
        if not await self.user_service.check_user_permission(
            current_user.id, "update_roles_permission"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update roles",
            )
        return await self.data_access.update_role_permissions(role_id, permissions)

RoleServiceDep = Annotated[RoleService, Depends(RoleService)]
