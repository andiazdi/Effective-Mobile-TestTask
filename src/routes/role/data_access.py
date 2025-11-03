from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, update

from src.dependencies.database import DBSessionDep
from src.routes.role.models import Role, RoleAccess
from src.routes.role.schemas import RoleAccessSchema, RoleSchema


class RoleDataAccess:
    def __init__(self, db_session: DBSessionDep):
        self.db_session = db_session

    async def get_role_permissions(self, role_id: int) -> RoleAccessSchema:
        res = await self.db_session.execute(
            select(RoleAccess).where(RoleAccess.role_id == role_id)
        )
        role_access_obj = res.scalar_one_or_none()
        if role_access_obj is None:
            return None
        return RoleAccessSchema.model_validate(role_access_obj)

    async def get_roles_with_permissions(
        self,
    ) -> list[tuple[RoleSchema, RoleAccessSchema]]:
        res = await self.db_session.execute(
            select(Role, RoleAccess).join(RoleAccess, Role.id == RoleAccess.role_id)
        )

        roles_with_permissions = []
        for role, access in res.all():
            role_schema = RoleSchema.model_validate(role)
            access_schema = RoleAccessSchema.model_validate(access)
            roles_with_permissions.append((role_schema, access_schema))

        return roles_with_permissions

    async def update_role_permissions(
        self,
        role_id: int,
        permissions: RoleAccessSchema,
    ) -> RoleAccessSchema:
        await self.db_session.execute(
            select(RoleAccess).where(RoleAccess.role_id == role_id)
        )
        await self.db_session.execute(
            update(RoleAccess)
            .where(RoleAccess.role_id == role_id)
            .values(**permissions.model_dump())
        )
        await self.db_session.commit()
        return permissions


RoleDataAccessDep = Annotated[RoleDataAccess, Depends(RoleDataAccess)]
