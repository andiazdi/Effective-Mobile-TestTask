from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
