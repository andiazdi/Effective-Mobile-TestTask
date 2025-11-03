from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from src.routes.auth.schemas import UserRegister
from src.routes.user.data_access import UsersDataAccessDep
from src.routes.user.schemas import UserInDBSchema, UserSchema


class UserService:
    def __init__(self, user_data_access: UsersDataAccessDep):
        self.data_access = user_data_access

    async def get_users(self, current_user: UserSchema) -> list[UserSchema]:
        if not await self.check_user_permission(
            current_user.id,
            "read_users_permission",
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view users",
            )
        return [
            UserInDBSchema.model_validate(i)
            for i in (await self.data_access.get_users())
        ]

    async def get_user_by_username(
        self,
        username: str,
    ) -> UserInDBSchema:
        try:
            return UserInDBSchema.model_validate(
                await self.data_access.get_user_by_username(username)
            )
        except ValidationError:
            return None

    async def add_user(
        self,
        user: UserRegister,
        hashed_password: str,
        is_admin: bool,
    ) -> UserSchema:
        return await self.data_access.add_user(user, hashed_password, is_admin)

    async def check_user_permission(self, user_id: int, permission: str) -> bool:
        permissions = await self.data_access.get_user_permissions(user_id)
        return permissions.get(permission, False)


UserServiceDep = Annotated[UserService, Depends(UserService)]
