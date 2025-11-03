from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies.auth import AuthUserDep
from src.routes.auth.schemas import Token, UserRegister
from src.routes.auth.service import AuthServiceDep
from src.routes.user.schemas import UserSchema

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/login")
async def login(
    service: AuthServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    return await service.login(form_data)


@auth_router.post("/register")
async def register(
    service: AuthServiceDep,
    user_register: UserRegister,
) -> UserSchema:
    return await service.register(user_register)


@auth_router.get("/me")
async def get_me(user: AuthUserDep) -> UserSchema:
    return user


@auth_router.delete("/me")
async def delete_me(
        service: AuthServiceDep,
        user: AuthUserDep,
) -> None:
    return await service.deactivate_account(user)
