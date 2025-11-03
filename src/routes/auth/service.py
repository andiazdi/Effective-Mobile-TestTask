from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash

from src.config import settings
from src.routes.auth.schemas import Token, UserRegister
from src.routes.user.schemas import UserInDBSchema, UserSchema
from src.routes.user.service import UserServiceDep

SECRET_KEY = settings.JWT_SECRET_KEY  # settings.JWT_SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def __init__(self, user_service: UserServiceDep):
        self.user_service = user_service

    async def login(self, form_data: OAuth2PasswordRequestForm) -> Token:
        user = await self._authenticate_user(form_data.username, form_data.password)
        if not user or user.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")  # noqa: S106

    async def register(
        self,
        user_register_schema: UserRegister,
        is_admin: bool = False,
    ) -> UserSchema:
        user = await self.user_service.get_user_by_username(
            user_register_schema.username
        )
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        hashed_password = password_hash.hash(user_register_schema.password)
        return await self.user_service.add_user(
            user_register_schema, hashed_password, is_admin
        )

    async def deactivate_account(self, user: UserSchema) -> None:
        await self.user_service.data_access.deactivate_account(user.id)

    async def _authenticate_user(self, username: str, password: str) -> UserInDBSchema:
        user = await self.user_service.get_user_by_username(username)
        if not user or not password_hash.verify(password, user.hashed_password):
            return False
        return user

    def _create_access_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
