from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    full_name: str
    email: EmailStr
    registered_date: datetime
    role: str

    model_config = ConfigDict(from_attributes=True)


class UserInDBSchema(UserSchema):
    hashed_password: str
    is_active: bool
