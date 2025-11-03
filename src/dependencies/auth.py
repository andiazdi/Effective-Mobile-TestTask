from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from src.config import settings
from src.routes.auth.schemas import TokenData
from src.routes.user.schemas import UserInDBSchema, UserSchema
from src.routes.user.service import UserServiceDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserServiceDep,
) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as err:
        raise credentials_exception from err

    user = await user_service.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


AuthUserDep = Annotated[UserInDBSchema, Depends(get_current_user)]
