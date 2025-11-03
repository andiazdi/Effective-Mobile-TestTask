from fastapi import APIRouter

from src.routes.auth.dependencies import AuthUserDep
from src.routes.role.schemas import RoleAccessSchema
from src.routes.role.service import RoleServiceDep

role_router = APIRouter(prefix="/roles", tags=["roles"])


@role_router.get("/")
async def get_roles(
    service: RoleServiceDep,
    current_user: AuthUserDep,
):
    return await service.get_roles_with_permissions(current_user)


@role_router.get("/{role_id}")
async def get_role_permissions(
    role_id: int,
    service: RoleServiceDep,
    current_user: AuthUserDep,
):
    return await service.get_role_permissions(role_id, current_user)


@role_router.put("/{role_id}")
async def update_role_permissions(
    role_id: int,
    permissions: RoleAccessSchema,
    service: RoleServiceDep,
    current_user: AuthUserDep,
):
    return await service.update_role_permissions(
        role_id, permissions, current_user
    )
