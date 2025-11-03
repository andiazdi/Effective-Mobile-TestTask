from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy import select

from src.dependencies.database import DBSessionDep
from src.routes.auth.schemas import UserRegister
from src.routes.role.models import Role, RoleAccess
from src.routes.user.models import User
from src.routes.user.schemas import UserInDBSchema, UserSchema


class UserDataAccess:
    def __init__(self, db_session: DBSessionDep):
        self.db_session = db_session

    async def get_user_permissions(self, user_id: int) -> dict[str, bool]:
        res = await self.db_session.execute(select(User).where(User.id == user_id))
        user = res.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        res = await self.db_session.execute(
            select(RoleAccess).where(RoleAccess.role_id == user.role_id)
        )
        role_access = res.scalars().first()
        if not role_access:
            return {}

        return {
            c.name: getattr(role_access, c.name)
            for c in role_access.__table__.columns
            if c.name not in ("id", "role_id")
        }

    async def get_users(self) -> list[UserInDBSchema]:
        res = await self.db_session.execute(
            select(User, Role.name.label("role_name")).join(Role)
        )
        users = []
        for user_obj, role_name in res.all():
            try:
                users.append(
                    UserInDBSchema.model_validate(
                        {**user_obj.__dict__, "role": role_name}
                    )
                )
            except ValidationError:
                continue
        return users

    async def get_user_by_username(self, username: str) -> UserInDBSchema | None:
        res = await self.db_session.execute(
            select(User, Role.name.label("role_name")).
            join(Role).where(User.username == username)
        )
        row = res.first()
        if row is None:
            return None
        user, role_name = row
        try:
            return UserInDBSchema.model_validate(
                {
                    **user.__dict__,
                    "role": role_name,
                }
            )
        except ValidationError:
            return None

    async def get_user_by_id(self, user_id: int) -> UserInDBSchema | None:
        res = await self.db_session.execute(
            select(User, Role.name.label("role_name")).
            join(Role).where(User.id == user_id)
        )
        row = res.first()
        if row is None:
            return None
        user, role_name = row
        try:
            return UserSchema.model_validate(
                {
                    **user.__dict__,
                    "role": role_name,
                }
            )
        except ValidationError:
            return None

    async def add_user(
        self,
        user: UserRegister,
        hashed_password: str,
        is_admin: bool,
    ) -> UserSchema:
        user_obj = User(**user.model_dump(exclude={"password"}))
        user_obj.hashed_password = hashed_password
        role = "user"
        if is_admin:
            role = "admin"
        role_obj = (
            (await self.db_session.execute(select(Role).where(Role.name == role)))
            .scalars()
            .first()
        )
        user_obj.role_id = role_obj.id
        self.db_session.add(user_obj)
        await self.db_session.commit()
        await self.db_session.refresh(user_obj)
        return UserSchema.model_validate(
            {
                **user_obj.__dict__,
                "role": role_obj.name,
            }
        )

    async def deactivate_account(self, user_id: int) -> None:
        user = await self.db_session.get(User, user_id)
        user.is_active = 0
        await self.db_session.commit()
        await self.db_session.refresh(user)


UsersDataAccessDep = Annotated[UserDataAccess, Depends(UserDataAccess)]
