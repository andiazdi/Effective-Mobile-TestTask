from fastapi import APIRouter

from src.dependencies.auth import AuthUserDep
from src.routes.user.schemas import UserSchema
from src.routes.user.service import UserServiceDep

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/")
async def get_users(
    service: UserServiceDep,
    current_user: AuthUserDep,
) -> list[UserSchema]:
    return await service.get_users(current_user)
